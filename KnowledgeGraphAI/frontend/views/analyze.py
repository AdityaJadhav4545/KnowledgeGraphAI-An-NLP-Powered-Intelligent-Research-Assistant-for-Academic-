"""Analyze Document view — Industrial / Architectural research ingestion workspace."""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional

import streamlit as st

from KnowledgeGraphAI.frontend.components.api_client import APIClient
from KnowledgeGraphAI.frontend.components.theme import escape_text, get_tokens, init_theme, toggle_theme
from KnowledgeGraphAI.frontend.components.ui import (
    render_entity_badge,
    render_error_panel,
    render_global_header,
    render_metric_cards,
    render_processing_pipeline,
    render_section_heading,
    render_status_badge,
)

MAX_UPLOAD_BYTES = 50 * 1024 * 1024
MIN_TEXT_CHARS = 10
MAX_TEXT_CHARS = 200_000


def _format_bytes(num_bytes: int) -> str:
    if num_bytes < 1024:
        return f"{num_bytes} B"
    if num_bytes < 1024 * 1024:
        return f"{num_bytes / 1024:.1f} KB"
    return f"{num_bytes / (1024 * 1024):.2f} MB"


def _clear_pending_inputs() -> None:
    st.session_state["pdf_uploader_nonce"] = int(st.session_state.get("pdf_uploader_nonce", 0)) + 1
    st.session_state["_clear_text_fields"] = True


def render(
    api_client: APIClient,
    on_navigate: Callable[[str], None],
    active_doc: Optional[Dict[str, Any]] = None,
) -> None:
    theme_name = init_theme()
    t = get_tokens(theme_name)

    if st.session_state.pop("reset_analyze_inputs", False):
        _clear_pending_inputs()

    if st.session_state.pop("_clear_text_fields", False):
        st.session_state["analyze_text_title"] = ""
        st.session_state["analyze_text_body"] = ""

    render_global_header(
        "Analyze Research",
        "Transform research documents into structured knowledge and discover meaningful relationships.",
        eyebrow="01 // DOCUMENT INGESTION & PIPELINE",
        active_doc=active_doc,
        theme_name=theme_name,
        on_toggle_theme=toggle_theme,
        action_label="Explore Active" if active_doc else None,
        action_key="analyze_header_explore_btn" if active_doc else None,
    )
    if active_doc and st.session_state.get("analyze_header_explore_btn"):
        on_navigate("Explore Knowledge")

    mode_tab_pdf, mode_tab_text = st.tabs(["Upload PDF", "Paste Text"])

    with mode_tab_pdf:
        render_section_heading(
            "PDF Input",
            "Research Paper Upload",
            "Select or drag a scientific PDF (up to 50 MB) to extract entities, relations, and indexed passages.",
        )

        nonce = int(st.session_state.get("pdf_uploader_nonce", 0))
        uploaded_file = st.file_uploader(
            "Drag and drop a PDF file or browse local files",
            type=["pdf"],
            accept_multiple_files=False,
            key=f"analyze_pdf_uploader_{nonce}",
            help="Supports text-based research papers and technical reports up to 50 MB.",
        )

        pdf_valid = False
        if uploaded_file is not None:
            raw_bytes = uploaded_file.getvalue()
            size_bytes = len(raw_bytes)
            lower_name = uploaded_file.name.lower()

            meta_col, action_col = st.columns([3.5, 1.0], vertical_alignment="center")
            with meta_col:
                if not lower_name.endswith(".pdf"):
                    validation_badge = render_status_badge("failed", theme_name)
                    validation_note = "Unsupported extension — upload a .pdf document."
                elif size_bytes == 0:
                    validation_badge = render_status_badge("failed", theme_name)
                    validation_note = "File appears empty (0 bytes)."
                elif size_bytes > MAX_UPLOAD_BYTES:
                    validation_badge = render_status_badge("failed", theme_name)
                    validation_note = f"Exceeds 50 MB limit ({_format_bytes(size_bytes)})."
                else:
                    validation_badge = render_status_badge("ready", theme_name)
                    validation_note = "PDF validated and staged for pipeline execution."
                    pdf_valid = True

                st.markdown(
                    f"""
                    <div class="kg-card" style="padding:0.85rem 1rem; margin-bottom:0.65rem;">
                        <div style="display:flex; align-items:center; justify-content:space-between; gap:0.5rem; margin-bottom:0.35rem;">
                            <span style="font-weight:600; color:{t['text_primary']};">{escape_text(uploaded_file.name)}</span>
                            {validation_badge}
                        </div>
                        <div class="kg-mono" style="font-size:0.78rem; color:{t['text_secondary']};">
                            SIZE: {_format_bytes(size_bytes)} &middot; {escape_text(validation_note)}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with action_col:
                if st.button("Remove File", key="remove_staged_pdf_btn", use_container_width=True):
                    _clear_pending_inputs()
                    st.rerun()

        optional_pdf_title = st.text_input(
            "Document Title Override (optional)",
            key="analyze_pdf_title_override",
            placeholder="Leave blank to infer title automatically from PDF metadata / first page",
        )

        run_pdf = st.button(
            "Generate Analysis",
            key="run_pdf_analysis_btn",
            type="primary",
            disabled=not pdf_valid,
            use_container_width=True,
        )

        if run_pdf and uploaded_file is not None and pdf_valid:
            stage_slot = st.empty()
            with stage_slot.container():
                render_section_heading("Pipeline Execution", "Running Knowledge Graph Pipeline")
                render_processing_pipeline(
                    completed=False,
                    active_index=0,
                    stage_note="Executing extraction, entity & relation mining, graph storage, and semantic indexing...",
                    theme_name=theme_name,
                )
            with st.spinner("Processing PDF through NLP, Knowledge Graph, and FAISS pipeline..."):
                raw_bytes = uploaded_file.getvalue()
                files = {"file": (uploaded_file.name, raw_bytes, "application/pdf")}
                data = {"title": optional_pdf_title.strip()} if optional_pdf_title.strip() else None
                res = api_client.post("/api/analyses/pdf", data=data, files=files, timeout=300)

            stage_slot.empty()
            if res.ok and isinstance(res.data, dict):
                st.session_state["_pending_selected_analysis_id"] = res.data["analysis_id"]
                st.session_state["last_completed_analysis"] = res.data
                st.rerun()
            else:
                render_error_panel("PDF Analysis Failed", res.error or "Unexpected error while analyzing PDF.")

    with mode_tab_text:
        render_section_heading(
            "Direct Text Input",
            "Paste Research Excerpt or Abstract",
            "Analyze paragraphs, methods sections, or technical notes directly without uploading a file.",
        )
        pasted_title = st.text_input(
            "Document Title (optional)",
            key="analyze_text_title",
            placeholder="e.g., Efficient Estimation of Word Representations in Vector Space",
        )
        pasted_text = st.text_area(
            "Research Content",
            key="analyze_text_body",
            height=240,
            placeholder=(
                "Paste a research abstract, methodology excerpt, or full article text here...\n\n"
                "Example: CBOW and Skip-gram were evaluated on the Google News dataset using Adagrad "
                "to measure syntactic and semantic word accuracy."
            ),
        )
        clean_len = len(pasted_text.strip())
        char_note = f"{clean_len:,} / {MAX_TEXT_CHARS:,} characters"
        if 0 < clean_len < MIN_TEXT_CHARS:
            char_note += f" (minimum {MIN_TEXT_CHARS} characters required)"
        elif clean_len > MAX_TEXT_CHARS:
            char_note += " (exceeds maximum text limit)"
        st.markdown(
            f'<div class="kg-mono" style="font-size:0.75rem; color:{t["text_secondary"]}; margin-bottom:0.65rem;">{char_note}</div>',
            unsafe_allow_html=True,
        )

        text_valid = MIN_TEXT_CHARS <= clean_len <= MAX_TEXT_CHARS
        run_text = st.button(
            "Generate Analysis",
            key="run_text_analysis_btn",
            type="primary",
            disabled=not text_valid,
            use_container_width=True,
        )

        if run_text and text_valid:
            stage_slot = st.empty()
            with stage_slot.container():
                render_section_heading("Pipeline Execution", "Running Knowledge Graph Pipeline")
                render_processing_pipeline(
                    completed=False,
                    active_index=2,
                    stage_note="Extracting scientific entities, relationships, graph structure, and embeddings...",
                    theme_name=theme_name,
                )
            with st.spinner("Constructing knowledge graph and indexing text passages..."):
                payload = {
                    "text": pasted_text.strip(),
                    "title": pasted_title.strip() or None,
                }
                res = api_client.post("/api/analyses/text", json_body=payload, timeout=180)

            stage_slot.empty()
            if res.ok and isinstance(res.data, dict):
                st.session_state["_pending_selected_analysis_id"] = res.data["analysis_id"]
                st.session_state["last_completed_analysis"] = res.data
                st.rerun()
            else:
                render_error_panel("Text Analysis Failed", res.error or "Unexpected error while analyzing text.")

    # Overview panel for newly finished or currently active document
    result = st.session_state.get("last_completed_analysis") or active_doc
    if result and isinstance(result, dict):
        st.markdown(
            f'<div style="border-top:1px solid {t["border"]}; margin:1.35rem 0 1rem 0;"></div>',
            unsafe_allow_html=True,
        )
        render_section_heading(
            "Analysis Overview",
            str(result.get("title") or "Untitled Document"),
            "Completed pipeline stages and extracted knowledge graph summary for the active workspace document.",
        )

        render_metric_cards(
            [
                ("Total Entities", result.get("entity_count", 0), "Unique normalized nodes"),
                ("Total Relationships", result.get("relationship_count", 0), "Directed semantic edges"),
                ("Entity Categories", result.get("category_count", 0), "Scientific domain classes"),
                ("Passages Processed", result.get("passage_count", 0), "Indexed evidence chunks"),
            ]
        )

        left_summary, right_pipeline = st.columns([1.35, 1.0], gap="medium")
        with left_summary:
            src_label = "PDF Research Paper" if result.get("source_type") == "pdf" else "Pasted Text Document"
            author_line = result.get("author") or "Not explicitly listed in document"
            pages_info = f"{result.get('page_count', 1)} page(s)" if result.get("source_type") == "pdf" else "Text segment source"
            entities = result.get("entities") or []
            badges_html = " ".join(
                render_entity_badge(str(ent.get("label") or ""), str(ent.get("category") or "Concept"), theme_name)
                for ent in entities[:12]
            )
            if not badges_html:
                badges_html = f'<span class="kg-muted">No normalized entities extracted from this excerpt.</span>'

            st.markdown(
                f"""
                <div class="kg-card" style="height:100%;">
                    <div class="kg-section-kicker">Document Summary</div>
                    <div style="display:flex; justify-content:space-between; align-items:center; gap:0.5rem; margin-bottom:0.55rem;">
                        <span class="kg-mono" style="font-size:0.76rem; color:{t['text_secondary']};">{src_label} &middot; {pages_info}</span>
                        {render_status_badge(str(result.get("status") or "completed"), theme_name)}
                    </div>
                    <div style="font-size:0.86rem; color:{t['text_secondary']}; margin-bottom:0.75rem;">
                        <strong style="color:{t['text_primary']};">Author(s):</strong> {escape_text(author_line)}
                    </div>
                    <div class="kg-section-kicker" style="margin-top:0.5rem;">Key Extracted Entities</div>
                    <div style="display:flex; flex-wrap:wrap; gap:0.35rem; margin-top:0.4rem;">
                        {badges_html}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with right_pipeline:
            render_processing_pipeline(
                completed=(str(result.get("status") or "").lower() == "completed"),
                stage_note="All pipeline stages executed against the backend API.",
                theme_name=theme_name,
            )

        cta_left, cta_right, _ = st.columns([1.2, 1.2, 2.0])
        with cta_left:
            if st.button("Open in Explore Knowledge ->", key="cta_go_explore", type="primary", use_container_width=True):
                on_navigate("Explore Knowledge")
        with cta_right:
            if st.button("Preview Academic Report", key="cta_go_report", use_container_width=True):
                on_navigate("Generate Report")
