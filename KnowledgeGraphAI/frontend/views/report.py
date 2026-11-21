"""Generate Report view — Typeset academic publication preview and PDF export."""

from __future__ import annotations

import base64
from typing import Any, Callable, Dict, List, Optional

import streamlit as st
import streamlit.components.v1 as components

from KnowledgeGraphAI.frontend.components.api_client import APIClient
from KnowledgeGraphAI.frontend.components.theme import (
    escape_text,
    get_entity_color,
    get_tokens,
    init_theme,
    toggle_theme,
)
from KnowledgeGraphAI.frontend.components.ui import (
    render_empty_state,
    render_error_panel,
    render_global_header,
)


def _provenance_pill(label: str, color: str) -> str:
    return (
        f'<span class="kg-badge" style="margin-left:0.5rem; font-size:0.68rem;">'
        f'<span class="kg-badge-dot" style="background-color:{color};"></span>'
        f"{escape_text(label)}"
        f"</span>"
    )


def _render_print_button(theme_name: str) -> None:
    t = get_tokens(theme_name)
    components.html(
        f"""
        <button
            onclick="window.parent.print()"
            style="
                width: 100%;
                height: 38px;
                border-radius: 6px;
                border: 1px solid {t['border']};
                background-color: {t['surface_elevated']};
                color: {t['text_primary']};
                font-family: Inter, -apple-system, BlinkMacSystemFont, sans-serif;
                font-size: 0.87rem;
                font-weight: 500;
                cursor: pointer;
            "
            title="Print formatted academic report (Ctrl+P)"
        >Print Report</button>
        """,
        height=44,
    )


def render(
    api_client: APIClient,
    analysis: Optional[Dict[str, Any]],
    on_navigate: Optional[Callable[[str], None]] = None,
) -> None:
    theme_name = init_theme()
    t = get_tokens(theme_name)

    action_clicked = render_global_header(
        "Generate Report",
        "Structured academic analysis report grounded in extracted entities, relationships, and document passages.",
        eyebrow="03 // PUBLICATION & EXPORT",
        active_doc=analysis,
        theme_name=theme_name,
        on_toggle_theme=toggle_theme,
        action_label="<- Explore Knowledge" if analysis else None,
        action_key="report_header_explore_btn" if analysis else None,
    )
    if action_clicked and on_navigate:
        on_navigate("Explore Knowledge")

    if not analysis:
        render_empty_state(
            "No Active Document Selected",
            "Analyze a PDF or pasted text first to compile and export a downloadable PDF research report.",
            kicker="Generate Report",
        )
        if on_navigate and st.button("Go to Analyze Document", key="report_empty_nav_btn", type="primary"):
            on_navigate("Analyze Document")
        return

    aid = analysis["analysis_id"]
    refresh_key = f"refresh_report_{aid}"
    refresh_flag = bool(st.session_state.pop(refresh_key, False))
    query_suffix = "?refresh=true" if refresh_flag else ""

    with st.spinner("Compiling structured report and academic PDF..."):
        rep_res = api_client.get(f"/api/analyses/{aid}/report{query_suffix}", timeout=120)
        pdf_res = api_client.get(f"/api/analyses/{aid}/report/pdf{query_suffix}", timeout=120)
        img_res = api_client.get(f"/api/analyses/{aid}/graph/image", timeout=60)

    if not rep_res.ok or not isinstance(rep_res.data, dict):
        render_error_panel("Report Generation Failed", rep_res.error or "Unable to compile analysis report.")
        return

    report = rep_res.data
    info = report.get("document_information") or {}
    kg_summary = report.get("knowledge_graph_summary") or {}
    entities: List[Dict[str, Any]] = list(report.get("key_concepts_and_entities") or [])
    relationships: List[Dict[str, Any]] = list(report.get("important_relationships") or [])
    references: List[Dict[str, Any]] = list(report.get("references_and_traceability") or [])

    safe_title_slug = "".join(c if c.isalnum() or c in "-_" else "_" for c in str(info.get("title") or "report"))[:50]
    pdf_bytes = pdf_res.data if (pdf_res.ok and isinstance(pdf_res.data, (bytes, bytearray))) else None

    # Action Toolbar
    dl_col, regen_col, print_col, spacer_col = st.columns([1.35, 1.05, 0.95, 1.45], vertical_alignment="center")
    with dl_col:
        if pdf_bytes:
            st.download_button(
                "Download PDF Report",
                data=bytes(pdf_bytes),
                file_name=f"KnowledgeGraphAI_{safe_title_slug}.pdf",
                mime="application/pdf",
                type="primary",
                key=f"download_pdf_{aid}",
                use_container_width=True,
            )
        else:
            st.button("PDF Unavailable", disabled=True, key=f"download_pdf_dis_{aid}", use_container_width=True)
    with regen_col:
        if st.button("Regenerate Report", key=f"regen_report_btn_{aid}", use_container_width=True):
            st.session_state[refresh_key] = True
            st.rerun()
    with print_col:
        _render_print_button(theme_name)
    with spacer_col:
        gen_time = str(report.get("generated_at") or "").replace("T", " ").replace(" UTC", "").strip()[:16]
        st.markdown(
            f'<div class="kg-mono" style="text-align:right; font-size:0.74rem; color:{t["text_secondary"]};">'
            f"COMPILED: {escape_text(gen_time)} UTC</div>",
            unsafe_allow_html=True,
        )

    # Embedded graph image base64
    graph_img_html = ""
    if img_res.ok and isinstance(img_res.data, (bytes, bytearray)):
        encoded_png = base64.b64encode(bytes(img_res.data)).decode("ascii")
        graph_img_html = (
            f'<div style="margin:0.75rem 0 0.25rem 0; border:1px solid {t["border"]}; border-radius:6px; overflow:hidden; background:#FFFFFF;">'
            f'<img src="data:image/png;base64,{encoded_png}" alt="Knowledge Graph Diagram" style="width:100%; height:auto; display:block;" />'
            f"</div>"
        )
    else:
        graph_img_html = f'<div class="kg-muted">Graph visualization image unavailable for this document.</div>'

    # Provenance Pills
    p_stated = _provenance_pill("Source-Stated Fact", t["success"])
    p_graph = _provenance_pill("Extracted Graph Relation", t["accent"])
    p_inferred = _provenance_pill("Analysis Synthesis", t["info"])

    # Section 4 table rows
    if entities:
        ent_rows_html = "".join(
            f"<tr>"
            f'<td><span class="kg-badge-dot" style="background-color:{get_entity_color(str(item.get("category") or "Concept"), theme_name)}; margin-right:0.4rem;"></span>'
            f'<strong>{escape_text(item.get("entity"))}</strong></td>'
            f'<td class="kg-mono">{escape_text(item.get("category"))}</td>'
            f'<td class="kg-mono">{escape_text(item.get("occurrences"))}</td>'
            f'<td>{escape_text(item.get("description"))}</td>'
            f"</tr>"
            for item in entities[:20]
        )
        entities_block = (
            '<table class="kg-report-table">'
            "<thead><tr><th>Entity</th><th>Category</th><th>Mentions</th><th>Source Context</th></tr></thead>"
            f"<tbody>{ent_rows_html}</tbody></table>"
        )
    else:
        entities_block = f'<p class="kg-muted">No normalized scientific entities were identified in this document.</p>'

    # Section 6 relationship table rows
    if relationships:
        rel_rows_html = "".join(
            f"<tr>"
            f'<td><strong>{escape_text(r.get("subject"))}</strong></td>'
            f'<td class="kg-mono" style="color:{t["accent"]};">{escape_text(r.get("relationship"))}</td>'
            f'<td><strong>{escape_text(r.get("object"))}</strong></td>'
            f'<td class="kg-mono">{escape_text(r.get("source"))}</td>'
            f"</tr>"
            for r in relationships[:30]
        )
        rel_block = (
            '<table class="kg-report-table">'
            "<thead><tr><th>Subject</th><th>Relationship</th><th>Object</th><th>Source</th></tr></thead>"
            f"<tbody>{rel_rows_html}</tbody></table>"
        )
    else:
        rel_block = f'<p class="kg-muted">No validated entity relationships were extracted from this document.</p>'

    # Section 11 traceability table rows
    if references:
        ref_rows_html = "".join(
            f"<tr>"
            f'<td class="kg-mono" style="color:{t["accent"]};">{escape_text(rf.get("ref"))}</td>'
            f"<td>{escape_text(rf.get('section'))}</td>"
            f"<td>{escape_text(rf.get('excerpt'))}</td>"
            f"</tr>"
            for rf in references[:12]
        )
        refs_block = (
            '<table class="kg-report-table">'
            "<thead><tr><th>Reference</th><th>Section</th><th>Source Excerpt</th></tr></thead>"
            f"<tbody>{ref_rows_html}</tbody></table>"
        )
    else:
        refs_block = f'<p class="kg-muted">No source passages recorded.</p>'

    # Render full academic typeset document preview sheet
    html_report = f"""
    <article class="kg-report-paper">
        <header class="kg-report-banner">
            <div class="kg-section-kicker">KnowledgeGraphAI // Academic Research Report</div>
            <h2 style="margin:0.15rem 0 0.45rem 0; font-size:1.55rem; line-height:1.25;">{escape_text(info.get('title') or 'Untitled Document')}</h2>
            <div class="kg-mono" style="font-size:0.76rem; color:{t['text_secondary']}; margin-bottom:0.55rem;">
                ANALYSIS ID: {escape_text(aid)} &middot; SOURCE: {escape_text(info.get('source_type'))} &middot; DATE: {escape_text(info.get('analysis_date'))}
            </div>
            <div style="display:flex; flex-wrap:wrap; align-items:center; gap:0.35rem; font-size:0.75rem; color:{t['text_secondary']};">
                <span>PROVENANCE KEY:</span>{p_stated}{p_graph}{p_inferred}
            </div>
        </header>

        <section class="kg-report-section" style="border-top:none; padding-top:0; margin-top:0;">
            <h3>1. Document Information {p_stated}</h3>
            <table class="kg-report-table">
                <thead><tr><th style="width:28%;">Metadata Field</th><th>Recorded Value</th></tr></thead>
                <tbody>
                    <tr><td>Title</td><td><strong>{escape_text(info.get('title'))}</strong></td></tr>
                    <tr><td>Authors</td><td>{escape_text(info.get('authors'))}</td></tr>
                    <tr><td>Publication / Source</td><td>{escape_text(info.get('publication_info'))}</td></tr>
                    <tr><td>Source Type</td><td class="kg-mono">{escape_text(info.get('source_type'))}</td></tr>
                    <tr><td>Date of Analysis</td><td class="kg-mono">{escape_text(info.get('analysis_date'))}</td></tr>
                </tbody>
            </table>
        </section>

        <section class="kg-report-section">
            <h3>2. Executive Summary {p_inferred}</h3>
            <p style="line-height:1.62; white-space:pre-wrap;">{escape_text(report.get('executive_summary'))}</p>
        </section>

        <section class="kg-report-section">
            <h3>3. Introduction and Main Objective {p_inferred}</h3>
            <p style="line-height:1.62; white-space:pre-wrap;">{escape_text(report.get('introduction_and_objective'))}</p>
        </section>

        <section class="kg-report-section">
            <h3>4. Key Concepts and Entities {p_graph}</h3>
            {entities_block}
        </section>

        <section class="kg-report-section">
            <h3>5. Knowledge Graph {p_graph}</h3>
            <p style="line-height:1.6;">
                Extracted <strong>{escape_text(kg_summary.get('total_entities', 0))}</strong> entities across
                <strong>{escape_text(kg_summary.get('category_count', 0))}</strong> domain categories and
                <strong>{escape_text(kg_summary.get('total_relationships', 0))}</strong> validated relationships.
            </p>
            {graph_img_html}
        </section>

        <section class="kg-report-section">
            <h3>6. Important Relationships {p_graph}</h3>
            {rel_block}
        </section>

        <section class="kg-report-section">
            <h3>7. Methodology and Techniques {p_inferred}</h3>
            <p style="line-height:1.62; white-space:pre-wrap;">{escape_text(report.get('methodology_and_techniques'))}</p>
        </section>

        <section class="kg-report-section">
            <h3>8. Important Findings {p_inferred}</h3>
            <p style="line-height:1.62; white-space:pre-wrap;">{escape_text(report.get('important_findings'))}</p>
        </section>

        <section class="kg-report-section">
            <h3>9. Limitations {p_stated}</h3>
            <p style="line-height:1.62; white-space:pre-wrap;">{escape_text(report.get('limitations'))}</p>
        </section>

        <section class="kg-report-section">
            <h3>10. Conclusion {p_inferred}</h3>
            <p style="line-height:1.62; white-space:pre-wrap;">{escape_text(report.get('conclusion'))}</p>
        </section>

        <section class="kg-report-section">
            <h3>11. References and Source Traceability {p_stated}</h3>
            {refs_block}
        </section>
    </article>
    """
    st.html(html_report)
