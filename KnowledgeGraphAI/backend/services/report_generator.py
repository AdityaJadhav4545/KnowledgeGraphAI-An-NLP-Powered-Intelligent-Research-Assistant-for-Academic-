"""Structured academic report & downloadable PDF generation for analyses."""

from __future__ import annotations

import io
import json
import logging
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import requests
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image as RLImage,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from sqlalchemy.orm import Session

from KnowledgeGraphAI.backend.config import Settings, get_settings
from KnowledgeGraphAI.models.analysis import AnalysisRecord

logger = logging.getLogger(__name__)

CATEGORY_COLORS = {
    "Model": "#4E6E58",
    "Algorithm": "#526474",
    "Dataset": "#6D7546",
    "Metric": "#726E65",
    "Task": "#3E6866",
    "Methodology": "#526474",
    "Framework": "#666352",
    "Optimizer": "#7F6440",
    "Organization": "#A1583F",
    "Author": "#686D65",
    "Paper": "#927744",
    "ResearchProblem": "#8F5938",
    "Concept": "#927744",
    "Technology": "#8F5938",
    "Person": "#9C6E44",
    "Group": "#4E6E58",
    "Project": "#3E6866",
    "Location": "#7C6447",
    "Product": "#647242",
}


def _xml_escape(text: str) -> str:
    return (
        str(text or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


class ReportGenerationService:
    """Build structured 11-section analysis reports and render academic PDFs."""

    def __init__(
        self,
        db: Session,
        *,
        settings: Optional[Settings] = None,
        http_session: Any = requests,
    ) -> None:
        self.db = db
        self.settings = settings or get_settings()
        self.http = http_session

    # ------------------------------------------------------------------
    # Graph diagram rendering (Matplotlib + NetworkX -> PNG bytes)
    # ------------------------------------------------------------------
    @staticmethod
    def render_graph_png(graph_json: Dict[str, Any], *, max_nodes: int = 32) -> bytes:
        nodes = list(graph_json.get("nodes") or [])[:max_nodes]
        node_ids = {n["id"] for n in nodes}
        edges = [
            e
            for e in (graph_json.get("edges") or [])
            if e.get("source") in node_ids and e.get("target") in node_ids
        ]

        fig, ax = plt.subplots(figsize=(8.5, 5.2), dpi=180)
        ax.set_facecolor("#F2F0E9")
        fig.patch.set_facecolor("#FFFFFF")

        if not nodes:
            ax.text(
                0.5,
                0.5,
                "No knowledge graph entities were extracted for this document.",
                ha="center",
                va="center",
                fontsize=11,
                color="#686D65",
            )
            ax.axis("off")
        else:
            g = nx.DiGraph()
            for n in nodes:
                g.add_node(n["id"], label=n["label"], category=n.get("category", "Entity"))
            for e in edges:
                g.add_edge(e["source"], e["target"], relation=e.get("relation", ""))

            k_val = 1.8 / max(1.0, len(nodes) ** 0.5)
            pos = nx.spring_layout(g, k=k_val, iterations=80, seed=42)

            node_colors = [
                CATEGORY_COLORS.get(g.nodes[nid]["category"], "#927744")
                for nid in g.nodes
            ]
            node_sizes = [
                max(420, min(1100, 420 + 120 * g.degree(nid)))
                for nid in g.nodes
            ]
            nx.draw_networkx_edges(
                g,
                pos,
                ax=ax,
                edge_color="#8E8A80",
                arrows=True,
                arrowsize=12,
                width=1.25,
                connectionstyle="arc3,rad=0.08",
            )
            nx.draw_networkx_nodes(
                g,
                pos,
                ax=ax,
                node_color=node_colors,
                node_size=node_sizes,
                edgecolors="#FFFFFF",
                linewidths=1.6,
            )

            labels = {
                nid: (g.nodes[nid]["label"][:22] + "...")
                if len(g.nodes[nid]["label"]) > 25
                else g.nodes[nid]["label"]
                for nid in g.nodes
            }
            nx.draw_networkx_labels(
                g,
                pos,
                labels=labels,
                ax=ax,
                font_size=7.5,
                font_weight="bold",
                font_color="#252925",
                bbox={"boxstyle": "round,pad=0.18", "facecolor": "#FFFFFF", "edgecolor": "#D8D5CA", "alpha": 0.9},
            )

            if len(edges) <= 28:
                edge_labels = {
                    (u, v): d.get("relation", "")
                    for u, v, d in g.edges(data=True)
                    if d.get("relation")
                }
                nx.draw_networkx_edge_labels(
                    g,
                    pos,
                    edge_labels=edge_labels,
                    ax=ax,
                    font_size=6.2,
                    font_color="#535850",
                    bbox={"facecolor": "#F2F0E9", "edgecolor": "none", "alpha": 0.85},
                )

            # Category legend
            present_cats = sorted({g.nodes[nid]["category"] for nid in g.nodes})
            handles = [
                plt.Line2D(
                    [0], [0], marker="o", color="w", label=cat,
                    markerfacecolor=CATEGORY_COLORS.get(cat, "#927744"), markersize=7
                )
                for cat in present_cats[:10]
            ]
            if handles:
                ax.legend(
                    handles=handles,
                    loc="upper center",
                    bbox_to_anchor=(0.5, -0.02),
                    ncol=min(5, len(handles)),
                    frameon=False,
                    fontsize=7.5,
                )
            ax.axis("off")

        plt.tight_layout()
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=180, bbox_inches="tight")
        plt.close(fig)
        return buf.getvalue()

    # ------------------------------------------------------------------
    # Structured 11-Section Synthesis (Ollama + Extractive Fallback)
    # ------------------------------------------------------------------
    @staticmethod
    def _section_text(sections: Sequence[Dict[str, Any]], names: Sequence[str]) -> str:
        targets = {n.casefold() for n in names}
        matched = [
            str(s.get("text") or "").strip()
            for s in sections
            if str(s.get("section_name") or "").casefold() in targets
        ]
        return "\n\n".join(m for m in matched if m)

    @staticmethod
    def _extract_sentences_matching(passages: Sequence[Dict[str, Any]], pattern: str, limit: int = 4) -> List[str]:
        hits: List[str] = []
        regex = re.compile(pattern, re.I)
        for p in passages:
            ref = p.get("source_ref") or "Source"
            for sent in re.split(r"(?<=[.!?])\s+", str(p.get("text") or "")):
                s = sent.strip()
                if len(s) >= 25 and regex.search(s):
                    hits.append(f"{s} ({ref})")
                if len(hits) >= limit:
                    return hits
        return hits

    def _synthesize_narratives(self, record: AnalysisRecord) -> Dict[str, str]:
        passages = list(record.passages_json or [])
        sections = list(record.sections_json or [])
        graph = record.graph_json or {}
        edges = list(graph.get("edges") or [])
        nodes = list(graph.get("nodes") or [])

        excerpt_text = "\n\n".join(
            f"[{p.get('source_ref', 'Source')}] {str(p.get('text') or '')[:700]}"
            for p in passages[:6]
        )
        rel_summary = "; ".join(
            f"{e['source_label']} {e['relation']} {e['target_label']} ({e.get('source_ref', '')})"
            for e in edges[:15]
        )

        # Try Ollama for clean academic prose (fast single JSON call, graceful fallback)
        prompt = (
            "You are preparing an academic research report strictly from the analyzed document.\n"
            "Return ONLY valid JSON with keys: executive_summary, introduction_objective, "
            "findings, source_limitations, conclusion.\n"
            "Do not invent facts, metrics, or citations absent from the text.\n\n"
            f"Title: {record.title}\n"
            f"Source Type: {record.source_type}\n"
            f"Key Entities: {', '.join(n['label'] for n in nodes[:15])}\n"
            f"Key Relationships: {rel_summary or 'None'}\n\n"
            f"Document Excerpts:\n{excerpt_text[:4500]}"
        )
        try:
            resp = self.http.post(
                f"{self.settings.ollama_base_url}/api/chat",
                json={
                    "model": self.settings.ollama_model,
                    "stream": False,
                    "format": "json",
                    "messages": [{"role": "user", "content": prompt}],
                    "options": {"temperature": 0.1, "num_predict": 450},
                },
                timeout=min(self.settings.ollama_timeout_seconds, 45),
            )
            resp.raise_for_status()
            parsed = json.loads(resp.json().get("message", {}).get("content", "{}"))
            if isinstance(parsed, dict) and parsed.get("executive_summary"):
                return {
                    "executive_summary": str(parsed.get("executive_summary", "")).strip(),
                    "introduction_objective": str(parsed.get("introduction_objective", "")).strip(),
                    "findings": str(parsed.get("findings", "")).strip(),
                    "source_limitations": str(parsed.get("source_limitations", "")).strip(),
                    "conclusion": str(parsed.get("conclusion", "")).strip(),
                }
        except Exception as exc:
            logger.info("Using deterministic extractive report synthesis: %s", exc)

        # Deterministic extractive fallback (grounded 100% in source)
        abstract_txt = self._section_text(sections, ("Abstract",))
        intro_txt = self._section_text(sections, ("Introduction",))
        conc_txt = self._section_text(sections, ("Conclusion", "Discussion"))

        first_passage = str(passages[0].get("text") or "") if passages else ""
        exec_summary = (abstract_txt or first_passage)[:900].strip()
        if not exec_summary:
            exec_summary = "No narrative text was available for summarization."

        intro_obj = (intro_txt or first_passage)[:900].strip()
        if not intro_obj:
            intro_obj = "Introduction and objective were not separated as a standalone section in this input."

        finding_sents = self._extract_sentences_matching(
            passages,
            r"\b(outperform|achiev|improv|result|show|demonstrate|observ|evaluat|accuracy|f1|bleu)\b",
            limit=4,
        )
        findings = (
            " ".join(finding_sents)
            if finding_sents
            else "No explicit quantitative findings were detected in the extracted passages."
        )

        lim_sents = self._extract_sentences_matching(
            passages,
            r"\b(limit|limitation|future work|drawback|challenge|impossible|difficult|cannot)\b",
            limit=3,
        )
        source_limits = (
            " ".join(lim_sents)
            if lim_sents
            else "No explicit limitations were stated in the analyzed text."
        )

        conclusion = (conc_txt or (str(passages[-1].get("text") or "") if passages else ""))[:900].strip()
        if not conclusion:
            conclusion = exec_summary

        return {
            "executive_summary": exec_summary,
            "introduction_objective": intro_obj,
            "findings": findings,
            "source_limitations": source_limits,
            "conclusion": conclusion,
        }

    def build_report_data(self, analysis_id: str, *, refresh: bool = False) -> Dict[str, Any]:
        record = (
            self.db.query(AnalysisRecord)
            .filter(AnalysisRecord.id == analysis_id)
            .first()
        )
        if record is None:
            raise KeyError(f"Analysis {analysis_id} not found")
        if record.status != "completed":
            raise ValueError("Analysis must complete before generating a report.")
        if record.report_json and not refresh:
            return record.report_json

        graph = record.graph_json or {"nodes": [], "edges": [], "stats": {}}
        nodes = list(graph.get("nodes") or [])
        edges = list(graph.get("edges") or [])
        stats = graph.get("stats") or {}
        passages = list(record.passages_json or [])

        narratives = self._synthesize_narratives(record)

        # Group methodology & technique categories
        tech_cats = ("Algorithm", "Model", "Framework", "Methodology", "Dataset", "Metric", "Optimizer")
        methodology_breakdown: Dict[str, List[str]] = {}
        for cat in tech_cats:
            items = [n["label"] for n in nodes if n.get("category") == cat]
            if items:
                methodology_breakdown[cat] = items

        inferred_limitations: List[str] = []
        if record.source_type == "text":
            inferred_limitations.append(
                "Input was provided as pasted text without PDF page boundaries or bibliographic metadata."
            )
        if not edges:
            inferred_limitations.append(
                "No schema-validated entity relationships co-occurred within the extracted sentences."
            )
        inferred_limitations.append(
            "Entity and relationship extraction relies on automated scientific rules and should be reviewed for domain-specific nuances."
        )

        report_data = {
            "analysis_id": record.id,
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "document_information": {
                "title": record.title,
                "authors": record.author or ("Not specified in pasted text" if record.source_type == "text" else "Not specified in PDF metadata"),
                "publication_info": record.publication_info or "Not available",
                "source_type": "PDF Document" if record.source_type == "pdf" else "Pasted Text",
                "analysis_date": record.created_at.strftime("%Y-%m-%d %H:%M UTC") if record.created_at else "",
            },
            "executive_summary": narratives["executive_summary"],
            "introduction_and_objective": narratives["introduction_objective"],
            "key_concepts_and_entities": [
                {
                    "entity": n["label"],
                    "category": n["category"],
                    "occurrences": n.get("occurrences", 1),
                    "description": f"Appears in {', '.join(n.get('source_refs', [])[:3]) or 'document'} — context: {n.get('sample_context', '')[:140]}",
                }
                for n in nodes[:30]
            ],
            "knowledge_graph_summary": {
                "total_entities": stats.get("total_entities", len(nodes)),
                "total_relationships": stats.get("total_relationships", len(edges)),
                "category_count": stats.get("category_count", 0),
                "categories": stats.get("categories", {}),
                "most_connected": stats.get("most_connected", [])[:5],
            },
            "important_relationships": [
                {
                    "subject": e.get("source_label", ""),
                    "relationship": e.get("relation", ""),
                    "object": e.get("target_label", ""),
                    "source": e.get("source_ref") or "Document",
                }
                for e in edges[:40]
            ],
            "methodology_and_techniques": methodology_breakdown,
            "important_findings": narratives["findings"],
            "limitations": {
                "source_stated": narratives["source_limitations"],
                "inferred_notes": inferred_limitations,
            },
            "conclusion": narratives["conclusion"],
            "references_and_traceability": [
                {
                    "ref": p.get("source_ref") or p.get("passage_id"),
                    "section": p.get("section_title") or "Body",
                    "excerpt": str(p.get("text") or "")[:240],
                }
                for p in passages[:15]
            ],
        }

        record.report_json = report_data
        self.db.commit()
        return report_data

    # ------------------------------------------------------------------
    # Academic PDF Rendering (ReportLab)
    # ------------------------------------------------------------------
    def generate_pdf_bytes(self, analysis_id: str, *, refresh: bool = False) -> bytes:
        report = self.build_report_data(analysis_id, refresh=refresh)
        record = self.db.query(AnalysisRecord).filter(AnalysisRecord.id == analysis_id).first()
        assert record is not None
        graph_png = self.render_graph_png(record.graph_json or {})

        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf,
            pagesize=LETTER,
            leftMargin=0.75 * inch,
            rightMargin=0.75 * inch,
            topMargin=0.85 * inch,
            bottomMargin=0.75 * inch,
            title=report["document_information"]["title"],
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=colors.HexColor("#252925"),
            spaceAfter=6,
        )
        subtitle_style = ParagraphStyle(
            "ReportSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#686D65"),
            spaceAfter=14,
        )
        h2_style = ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12.5,
            leading=16,
            textColor=colors.HexColor("#927744"),
            spaceBefore=14,
            spaceAfter=6,
        )
        body_style = ParagraphStyle(
            "ReportBody",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.8,
            leading=14,
            textColor=colors.HexColor("#252925"),
            spaceAfter=6,
        )
        cell_style = ParagraphStyle(
            "CellBody",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11.5,
            textColor=colors.HexColor("#252925"),
        )
        cell_hdr = ParagraphStyle(
            "CellHeader",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.8,
            leading=11.5,
            textColor=colors.white,
        )

        story: List[Any] = []
        info = report["document_information"]
        story.append(Paragraph(_xml_escape(info["title"]), title_style))
        story.append(
            Paragraph(
                _xml_escape(f"KnowledgeGraphAI Research Analysis Report · Generated {report['generated_at']}"),
                subtitle_style,
            )
        )

        def _styled_table(rows: List[List[Any]], col_widths: List[float]) -> Table:
            tbl = Table(rows, colWidths=col_widths, repeatRows=1)
            tbl.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#202321")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#E8E4DA")),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D8D5CA")),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F0E9")]),
                        ("LEFTPADDING", (0, 0), (-1, -1), 6),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                        ("TOPPADDING", (0, 0), (-1, -1), 5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ]
                )
            )
            return tbl

        # Section 1: Document Information
        story.append(Paragraph("1. Document Information", h2_style))
        info_rows = [
            [Paragraph("Field", cell_hdr), Paragraph("Details", cell_hdr)],
            [Paragraph("Title", cell_style), Paragraph(_xml_escape(info["title"]), cell_style)],
            [Paragraph("Authors", cell_style), Paragraph(_xml_escape(info["authors"]), cell_style)],
            [Paragraph("Publication / Source", cell_style), Paragraph(_xml_escape(info["publication_info"]), cell_style)],
            [Paragraph("Source Type", cell_style), Paragraph(_xml_escape(info["source_type"]), cell_style)],
            [Paragraph("Date of Analysis", cell_style), Paragraph(_xml_escape(info["analysis_date"]), cell_style)],
        ]
        story.append(_styled_table(info_rows, [1.8 * inch, 5.2 * inch]))
        story.append(Spacer(1, 8))

        # Section 2: Executive Summary
        story.append(Paragraph("2. Executive Summary", h2_style))
        story.append(Paragraph(_xml_escape(report["executive_summary"]), body_style))

        # Section 3: Introduction and Main Objective
        story.append(Paragraph("3. Introduction and Main Objective", h2_style))
        story.append(Paragraph(_xml_escape(report["introduction_and_objective"]), body_style))

        # Section 4: Key Concepts and Entities
        story.append(Paragraph("4. Key Concepts and Entities", h2_style))
        ent_list = report["key_concepts_and_entities"]
        if ent_list:
            ent_rows = [[
                Paragraph("Entity", cell_hdr),
                Paragraph("Category", cell_hdr),
                Paragraph("Freq", cell_hdr),
                Paragraph("Source Context", cell_hdr),
            ]]
            for item in ent_list[:20]:
                ent_rows.append([
                    Paragraph(_xml_escape(item["entity"]), cell_style),
                    Paragraph(_xml_escape(item["category"]), cell_style),
                    Paragraph(str(item["occurrences"]), cell_style),
                    Paragraph(_xml_escape(item["description"]), cell_style),
                ])
            story.append(_styled_table(ent_rows, [1.5 * inch, 1.0 * inch, 0.5 * inch, 4.0 * inch]))
        else:
            story.append(Paragraph("No domain entities matched in this document.", body_style))

        # Section 5: Knowledge Graph Visualization
        story.append(Paragraph("5. Knowledge Graph", h2_style))
        kg_sum = report["knowledge_graph_summary"]
        story.append(
            Paragraph(
                _xml_escape(
                    f"Extracted {kg_sum['total_entities']} unique entities across "
                    f"{kg_sum['category_count']} categories and {kg_sum['total_relationships']} validated relationships."
                ),
                body_style,
            )
        )
        img_stream = io.BytesIO(graph_png)
        story.append(RLImage(img_stream, width=6.8 * inch, height=4.15 * inch))
        story.append(Spacer(1, 6))

        # Section 6: Important Relationships
        story.append(Paragraph("6. Important Relationships", h2_style))
        rels = report["important_relationships"]
        if rels:
            rel_rows = [[
                Paragraph("Subject", cell_hdr),
                Paragraph("Relationship", cell_hdr),
                Paragraph("Object", cell_hdr),
                Paragraph("Source", cell_hdr),
            ]]
            for r in rels[:30]:
                rel_rows.append([
                    Paragraph(_xml_escape(r["subject"]), cell_style),
                    Paragraph(_xml_escape(r["relationship"]), cell_style),
                    Paragraph(_xml_escape(r["object"]), cell_style),
                    Paragraph(_xml_escape(r["source"]), cell_style),
                ])
            story.append(_styled_table(rel_rows, [1.9 * inch, 1.4 * inch, 2.3 * inch, 1.4 * inch]))
        else:
            story.append(Paragraph("No validated entity relationships were extracted from this document.", body_style))

        # Section 7: Methodology and Techniques
        story.append(Paragraph("7. Methodology and Techniques", h2_style))
        tech = report["methodology_and_techniques"]
        if tech:
            for cat, names in tech.items():
                story.append(
                    Paragraph(
                        f"<b>{_xml_escape(cat)}:</b> {_xml_escape(', '.join(names[:20]))}",
                        body_style,
                    )
                )
        else:
            story.append(Paragraph("No specific algorithms, models, datasets, or metrics were detected.", body_style))

        # Section 8: Important Findings
        story.append(Paragraph("8. Important Findings", h2_style))
        story.append(Paragraph(_xml_escape(report["important_findings"]), body_style))

        # Section 9: Limitations
        story.append(Paragraph("9. Limitations", h2_style))
        story.append(
            Paragraph(
                f"<b>Source-stated limitations:</b> {_xml_escape(report['limitations']['source_stated'])}",
                body_style,
            )
        )
        for note in report["limitations"]["inferred_notes"]:
            story.append(Paragraph(f"<b>Inferred scope note:</b> {_xml_escape(note)}", body_style))

        # Section 10: Conclusion
        story.append(Paragraph("10. Conclusion", h2_style))
        story.append(Paragraph(_xml_escape(report["conclusion"]), body_style))

        # Section 11: References and Source Traceability
        story.append(Paragraph("11. References and Source Traceability", h2_style))
        refs = report["references_and_traceability"]
        if refs:
            ref_rows = [[
                Paragraph("Reference", cell_hdr),
                Paragraph("Section", cell_hdr),
                Paragraph("Source Excerpt", cell_hdr),
            ]]
            for rf in refs[:12]:
                ref_rows.append([
                    Paragraph(_xml_escape(rf["ref"]), cell_style),
                    Paragraph(_xml_escape(rf["section"]), cell_style),
                    Paragraph(_xml_escape(rf["excerpt"]), cell_style),
                ])
            story.append(_styled_table(ref_rows, [1.3 * inch, 1.2 * inch, 4.5 * inch]))
        else:
            story.append(Paragraph("No source passages recorded.", body_style))

        short_title = (info["title"][:48] + "...") if len(info["title"]) > 51 else info["title"]

        def _draw_chrome(canvas_obj, doc_obj):
            canvas_obj.saveState()
            canvas_obj.setFont("Helvetica", 8)
            canvas_obj.setStrokeColor(colors.HexColor("#927744"))
            canvas_obj.setFillColor(colors.HexColor("#686D65"))
            canvas_obj.drawString(0.75 * inch, 10.45 * inch, f"KnowledgeGraphAI Research Report — {short_title}")
            canvas_obj.line(0.75 * inch, 10.35 * inch, 7.75 * inch, 10.35 * inch)
            canvas_obj.line(0.75 * inch, 0.55 * inch, 7.75 * inch, 0.55 * inch)
            canvas_obj.drawString(0.75 * inch, 0.38 * inch, f"Analysis ID: {analysis_id}")
            canvas_obj.drawRightString(7.75 * inch, 0.38 * inch, f"Page {doc_obj.page}")
            canvas_obj.restoreState()

        doc.build(story, onFirstPage=_draw_chrome, onLaterPages=_draw_chrome)
        return buf.getvalue()

