"""Reusable Industrial / Architectural UI components for KnowledgeGraphAI."""

from __future__ import annotations

import time
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

import streamlit as st

from KnowledgeGraphAI.frontend.components.theme import (
    escape_text,
    get_entity_color,
    get_tokens,
    init_theme,
)

PROCESSING_STAGES: List[Tuple[str, str]] = [
    ("01", "Document extraction"),
    ("02", "Text preprocessing"),
    ("03", "Entity extraction"),
    ("04", "Relationship extraction"),
    ("05", "Knowledge graph construction"),
    ("06", "Semantic indexing"),
]


def geometric_logo_svg(theme_name: str | None = None, size: int = 34) -> str:
    """Return a precision architectural geometric node-lattice SVG logo (no brain icon)."""
    t = get_tokens(theme_name)
    accent = t["accent"]
    stroke = t["text_primary"]
    bg = t["bg_main"]
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="KnowledgeGraphAI Geometric Mark">
      <rect x="2" y="2" width="32" height="32" rx="6" fill="{bg}" stroke="{t['border']}" stroke-width="1.4"/>
      <path d="M10 11L25 10L26 24L11 26L10 11Z" stroke="{stroke}" stroke-opacity="0.48" stroke-width="1.2"/>
      <path d="M10 11L18 18L25 10" stroke="{accent}" stroke-width="1.5"/>
      <path d="M18 18L26 24" stroke="{accent}" stroke-width="1.5"/>
      <path d="M18 18L11 26" stroke="{stroke}" stroke-opacity="0.6" stroke-width="1.2"/>
      <circle cx="10" cy="11" r="2.6" fill="{stroke}"/>
      <circle cx="25" cy="10" r="2.6" fill="{accent}"/>
      <circle cx="18" cy="18" r="3.1" fill="{accent}" stroke="{bg}" stroke-width="1"/>
      <circle cx="26" cy="24" r="2.4" fill="{stroke}"/>
      <circle cx="11" cy="26" r="2.4" fill="{stroke}"/>
    </svg>
    """


def render_brand_sidebar(theme_name: str | None = None) -> None:
    """Render brand identity block at the top of the sidebar."""
    svg = geometric_logo_svg(theme_name, size=34)
    st.markdown(
        f"""
        <div class="kg-brand-box">
            <div class="kg-brand-left">
                <div style="flex-shrink:0; display:flex;">{svg}</div>
                <div>
                    <div class="kg-brand-title">KnowledgeGraphAI</div>
                    <div class="kg-brand-tagline">Industrial. Precise. Intelligent.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_brand_header(
    theme_name: str | None = None,
    *,
    on_collapse: Optional[Callable[[], Any]] = None,
) -> None:
    """Render sidebar brand identity paired with a collapse button."""
    svg = geometric_logo_svg(theme_name, size=32)
    t = get_tokens(theme_name)
    brand_col, btn_col = st.columns([4.2, 1.0], vertical_alignment="center", gap="small")
    with brand_col:
        st.markdown(
            f"""
            <div class="kg-brand-left">
                <div style="flex-shrink:0; display:flex;">{svg}</div>
                <div style="min-width:0;">
                    <div class="kg-brand-title">KnowledgeGraphAI</div>
                    <div class="kg-brand-tagline">Industrial. Precise. Intelligent.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with btn_col:
        if on_collapse and st.button(
            "«",
            key="sidebar_collapse_btn",
            help="Collapse sidebar to expand workspace",
            use_container_width=True,
        ):
            on_collapse()
            st.rerun()
    st.markdown(
        f'<div style="border-bottom:1px solid {t["border"]}; margin:0.06rem 0 0.08rem 0;"></div>',
        unsafe_allow_html=True,
    )


def render_collapsed_sidebar_bar(
    theme_name: str,
    active_doc: Optional[Dict[str, Any]],
    *,
    on_expand: Callable[[], Any],
) -> None:
    """Render an accessible top bar to restore the collapsed sidebar."""
    t = get_tokens(theme_name)
    left_c, right_c = st.columns([1.3, 4.5], vertical_alignment="center", gap="small")
    with left_c:
        if st.button(
            "» Open Sidebar",
            key="sidebar_restore_btn",
            help="Restore workspace navigation, documents, and Ask Me assistant",
            use_container_width=True,
        ):
            on_expand()
            st.rerun()
    with right_c:
        title_txt = (
            escape_text(active_doc.get("title") or "Untitled Document")
            if active_doc
            else "No active document selected"
        )
        st.markdown(
            f'<div class="kg-mono" style="font-size:0.75rem; color:{t["text_secondary"]}; text-align:right;">'
            f'SIDEBAR COLLAPSED &middot; DOCUMENT: <strong style="color:{t["text_primary"]};">{title_txt}</strong></div>',
            unsafe_allow_html=True,
        )


def status_color(status: str, theme_name: str | None = None) -> str:
    """Map real document status strings to muted architectural colors."""
    t = get_tokens(theme_name)
    normalized = str(status or "").strip().lower()
    if normalized in {"completed", "ready"}:
        return t["success"]
    if normalized in {"processing", "running", "pending"}:
        return t["warning"]
    if normalized in {"failed", "error"}:
        return t["error"]
    return t["text_secondary"]


def render_status_badge(status: str, theme_name: str | None = None) -> str:
    """Build inline HTML for a document processing status badge."""
    clean = str(status or "unknown").strip().capitalize()
    dot = status_color(status, theme_name)
    return (
        f'<span class="kg-badge">'
        f'<span class="kg-badge-dot" style="background-color:{dot};"></span>'
        f"{escape_text(clean)}"
        f"</span>"
    )


def render_entity_badge(label: str, category: str, theme_name: str | None = None) -> str:
    """Build inline HTML for a domain-colored entity pill."""
    color = get_entity_color(category, theme_name)
    return (
        f'<span class="kg-badge" title="{escape_text(category)}">'
        f'<span class="kg-badge-dot" style="background-color:{color};"></span>'
        f"{escape_text(label)}"
        f"</span>"
    )


def render_global_header(
    page_title: str,
    subtitle: str,
    *,
    eyebrow: str,
    active_doc: Optional[Dict[str, Any]] = None,
    theme_name: str,
    on_toggle_theme: Callable[[], Any],
    action_label: Optional[str] = None,
    action_key: Optional[str] = None,
) -> bool:
    """Render consistent global workspace header with theme switch and optional quick action."""
    action_triggered = False
    t = get_tokens(theme_name)
    doc_pill_html = ""
    if active_doc:
        title = escape_text(active_doc.get("title") or "Untitled document")
        src = "PDF" if active_doc.get("source_type") == "pdf" else "Text"
        dot = status_color(str(active_doc.get("status") or ""), theme_name)
        doc_pill_html = (
            f'<div class="kg-active-doc-pill">'
            f'<span class="kg-status-dot" style="background-color:{dot};"></span>'
            f'<span>ACTIVE // {src}</span>'
            f'<span style="color:{t["text_secondary"]};">|</span>'
            f'<span style="font-weight:600; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:340px;">{title}</span>'
            f"</div>"
        )

    left_col, right_col = st.columns([2.65, 1.95], vertical_alignment="center")
    with left_col:
        st.markdown(
            f"""
            <div class="kg-header-left">
                <div class="kg-header-eyebrow">{escape_text(eyebrow)}</div>
                <h1 class="kg-header-title">{escape_text(page_title)}</h1>
                <p class="kg-header-subtitle">{escape_text(subtitle)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right_col:
        if doc_pill_html:
            st.markdown(
                f'<div style="display:flex; justify-content:flex-end; margin-bottom:0.45rem;">{doc_pill_html}</div>',
                unsafe_allow_html=True,
            )
        btn_cols = st.columns([1.05, 1.05] if action_label else [1.0])
        if action_label and action_key:
            with btn_cols[0]:
                if st.button(action_label, key=action_key, use_container_width=True):
                    action_triggered = True
            theme_col = btn_cols[1]
        else:
            theme_col = btn_cols[0]

        active_label = "Obsidian (Dark)" if theme_name == "obsidian" else "Limestone (Light)"
        next_label = "Limestone (Light)" if theme_name == "obsidian" else "Obsidian (Dark)"
        with theme_col:
            if st.button(
                f"Theme: {active_label}",
                key=f"theme_toggle_header_{action_key or eyebrow}",
                use_container_width=True,
                help=f"Active theme: {active_label}. Click to switch to {next_label}.",
            ):
                on_toggle_theme()
                st.rerun()

    st.markdown(
        f'<div style="border-bottom:1px solid {t["border"]}; margin:0.45rem 0 1.05rem 0;"></div>',
        unsafe_allow_html=True,
    )
    return action_triggered


def _metric_icon_svg(label: str, accent: str) -> str:
    low = label.lower()
    if "entit" in low:
        return (
            f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none">'
            f'<path d="M12 3L3 8L12 13L21 8L12 3Z" stroke="{accent}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<path d="M3 13L12 18L21 13" stroke="{accent}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
            f"</svg>"
        )
    if "relat" in low:
        return (
            f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none">'
            f'<path d="M10 14L14 10" stroke="{accent}" stroke-width="1.7" stroke-linecap="round"/>'
            f'<rect x="4" y="13" width="7" height="7" rx="2" stroke="{accent}" stroke-width="1.6"/>'
            f'<rect x="13" y="4" width="7" height="7" rx="2" stroke="{accent}" stroke-width="1.6"/>'
            f"</svg>"
        )
    if "categor" in low or "concept" in low:
        return (
            f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none">'
            f'<rect x="4" y="4" width="7" height="7" rx="1.5" stroke="{accent}" stroke-width="1.6"/>'
            f'<rect x="13" y="4" width="7" height="7" rx="1.5" stroke="{accent}" stroke-width="1.6"/>'
            f'<rect x="4" y="13" width="7" height="7" rx="1.5" stroke="{accent}" stroke-width="1.6"/>'
            f'<rect x="13" y="13" width="7" height="7" rx="1.5" stroke="{accent}" stroke-width="1.6"/>'
            f"</svg>"
        )
    return (
        f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none">'
        f'<path d="M6 3H14L19 8V21H6V3Z" stroke="{accent}" stroke-width="1.6" stroke-linejoin="round"/>'
        f'<path d="M14 3V8H19" stroke="{accent}" stroke-width="1.6" stroke-linejoin="round"/>'
        f"</svg>"
    )


def render_metric_cards(items: Iterable[Tuple[str, Any, str]]) -> None:
    """Render an evenly spaced row of equal-height architectural metric cards."""
    entries = list(items)
    if not entries:
        return
    t = get_tokens(init_theme())
    cols = st.columns(len(entries), gap="small")
    for col, (label, value, sub) in zip(cols, entries):
        icon_svg = _metric_icon_svg(label, t["accent"])
        with col:
            st.markdown(
                f"""
                <div class="kg-metric-card" title="{escape_text(sub)}">
                    <div class="kg-metric-icon">{icon_svg}</div>
                    <div class="kg-metric-body">
                        <div class="kg-metric-value">{escape_text(value)}</div>
                        <div class="kg-metric-label">{escape_text(label)}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_section_heading(kicker: str, title: str, subtitle: str = "") -> None:
    """Render consistent editorial section heading."""
    sub_html = f'<div class="kg-muted">{escape_text(subtitle)}</div>' if subtitle else ""
    st.markdown(
        f"""
        <div style="margin:0.35rem 0 0.65rem 0;">
            <div class="kg-section-kicker">{escape_text(kicker)}</div>
            <div class="kg-panel-title">{escape_text(title)}</div>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state(title: str, body: str, kicker: str = "Workspace State") -> None:
    """Render a framed empty-state panel."""
    st.markdown(
        f"""
        <div class="kg-card">
            <div class="kg-section-kicker">{escape_text(kicker)}</div>
            <div class="kg-panel-title">{escape_text(title)}</div>
            <div class="kg-muted">{escape_text(body)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_error_panel(title: str, message: str) -> None:
    """Render a disciplined error notification card."""
    t = get_tokens(init_theme())
    st.markdown(
        f"""
        <div class="kg-card" style="border-left:3px solid {t['error']};">
            <div class="kg-section-kicker" style="color:{t['error']};">Diagnostic Notice</div>
            <div class="kg-panel-title">{escape_text(title)}</div>
            <div class="kg-muted" style="color:{t['text_primary']};">{escape_text(message)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_processing_pipeline(
    completed: bool = False,
    active_index: int | None = None,
    stage_note: str | None = None,
    theme_name: str | None = None,
) -> None:
    """Render the real 6-stage NLP & knowledge graph processing steps without synthetic % bars."""
    t = get_tokens(theme_name)
    rows: List[str] = []
    for idx, (code, label) in enumerate(PROCESSING_STAGES):
        if completed:
            badge_text = "Completed"
            badge_color = t["success"]
        elif active_index is not None and idx < active_index:
            badge_text = "Completed"
            badge_color = t["success"]
        elif active_index is not None and idx == active_index:
            badge_text = "In progress"
            badge_color = t["accent"]
        else:
            badge_text = "Queued"
            badge_color = t["text_secondary"]
        rows.append(
            f'<div class="kg-stage-row">'
            f'<div><span class="kg-stage-index">{code}</span><span>{escape_text(label)}</span></div>'
            f'<span class="kg-badge" style="color:{badge_color};">'
            f'<span class="kg-badge-dot" style="background-color:{badge_color};"></span>{badge_text}'
            f"</span>"
            f"</div>"
        )
    note_html = (
        f'<div class="kg-muted" style="padding:0.55rem 0.72rem 0.15rem 0.72rem; font-size:0.8rem;">{escape_text(stage_note)}</div>'
        if stage_note
        else ""
    )
    st.markdown(
        f'<div class="kg-card" style="padding:0.55rem 0.45rem;">{"".join(rows)}{note_html}</div>',
        unsafe_allow_html=True,
    )


def render_boxed_ask_me(
    api_client: Any,
    active_doc: Optional[Dict[str, Any]],
    *,
    backend_ok: bool,
    on_attach_pdf: Callable[[], Any],
    theme_name: str | None = None,
) -> None:
    """Render the bordered Ask Me AI assistant card inside the lower sidebar."""
    t = get_tokens(theme_name)
    dot_color = t["success"] if backend_ok else t["error"]
    ai_label = "AI Online" if backend_ok else "AI Offline"

    assistant_icon_svg = (
        f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        f'<rect x="3" y="6" width="18" height="13" rx="4" stroke="{t["accent"]}" stroke-width="1.6"/>'
        f'<path d="M12 3V6" stroke="{t["accent"]}" stroke-width="1.6" stroke-linecap="round"/>'
        f'<circle cx="9" cy="12" r="1.4" fill="{t["text_primary"]}"/>'
        f'<circle cx="15" cy="12" r="1.4" fill="{t["text_primary"]}"/>'
        f'<path d="M9 15.5H15" stroke="{t["accent"]}" stroke-width="1.4" stroke-linecap="round"/>'
        f"</svg>"
    )

    with st.container(border=True, key="askme_card"):
        st.markdown(
            f"""
            <div class="kg-sidebar-chat-hdr">
                <span class="kg-sidebar-chat-title">{assistant_icon_svg}<span>Ask Me</span></span>
                <span class="kg-badge" style="font-size:0.66rem;">
                    <span class="kg-badge-dot" style="background-color:{dot_color};"></span>{ai_label}
                </span>
            </div>
            <div style="font-size:0.77rem; color:{t['text_secondary']}; margin-bottom:0.38rem;">
                Ask questions about your active document.
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not active_doc or not active_doc.get("analysis_id"):
            st.markdown(
                """
                <div class="kg-askme-empty">
                    Analyze or select a document above to ask grounded questions.
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(
                "Attach / Upload PDF",
                key="sidebar_askme_attach_empty_btn",
                use_container_width=True,
            ):
                on_attach_pdf()
            return

        aid = str(active_doc["analysis_id"])
        history: List[Dict[str, Any]] = list(active_doc.get("chat_history") or [])
        inflight_key = f"askme_inflight_{aid}"
        is_streaming = bool(st.session_state.get(inflight_key, False))

        def _live_turn_html(
            turn_num: int,
            question_txt: str,
            assistant_txt: str,
            status_txt: str,
            *,
            streaming_cursor: bool = False,
        ) -> str:
            cursor = " ▍" if streaming_cursor else ""
            return f"""
                <div class="kg-msg-user">
                    <div class="kg-msg-meta"><span>You</span><span>#{turn_num}</span></div>
                    <div>{escape_text(question_txt)}</div>
                </div>
                <div class="kg-msg-assistant">
                    <div class="kg-msg-meta"><span style="color:{t['accent']};">Assistant</span><span>{escape_text(status_txt)}</span></div>
                    <div style="white-space:pre-wrap;">{escape_text(assistant_txt)}{cursor}</div>
                </div>
            """

        empty_notice = None
        # Scrollable conversation area: compact empty state when empty, bounded scroll when messages exist
        with st.container(border=False, key="askme_messages"):
            if not history:
                empty_notice = st.empty()
                empty_notice.markdown(
                    f"""
                    <div class="kg-askme-empty">
                        Scoped to <strong style="color:{t['text_primary']};">{escape_text(active_doc.get('title') or 'active document')}</strong>. Ask about entities, methods, metrics, or findings.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                for idx, turn in enumerate(history):
                    q_txt = str(turn.get("question") or "")
                    a_txt = str(turn.get("answer") or "")
                    mode = str(turn.get("generation_mode") or "evidence").replace("_", " ").upper()
                    timing_info = turn.get("timing")
                    meta_badge = mode
                    if isinstance(timing_info, dict) and timing_info.get("total_ms"):
                        total_s = float(timing_info["total_ms"]) / 1000.0
                        meta_badge = f"{mode} · {total_s:.1f}s"
                    citations = turn.get("citations") or []
                    graph_ctx = turn.get("graph_context")
                    graph_rels = (
                        list(graph_ctx.get("relationships") or [])
                        if isinstance(graph_ctx, dict)
                        else (list(graph_ctx) if isinstance(graph_ctx, list) else [])
                    )

                    st.markdown(
                        f"""
                        <div class="kg-msg-user">
                            <div class="kg-msg-meta"><span>You</span><span>#{idx + 1}</span></div>
                            <div>{escape_text(q_txt)}</div>
                        </div>
                        <div class="kg-msg-assistant">
                            <div class="kg-msg-meta"><span style="color:{t['accent']};">Assistant</span><span>{escape_text(meta_badge)}</span></div>
                            <div style="white-space:pre-wrap;">{escape_text(a_txt)}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    c1, c2 = st.columns(2, gap="small")
                    with c1:
                        with st.popover("Copy", use_container_width=True):
                            st.code(a_txt, language=None)
                    with c2:
                        src_count = len(citations) + len(graph_rels)
                        with st.popover(f"Sources ({src_count})", use_container_width=True):
                            for c_idx, cit in enumerate(citations[:5]):
                                ref_id = cit.get("citation_id") or f"S{c_idx + 1}"
                                ref_loc = cit.get("source_ref") or f"Page {cit.get('page_number', '?')}"
                                excerpt = str(cit.get("passage") or "")[:240]
                                st.markdown(
                                    f'<div class="kg-citation-card"><span class="kg-citation-ref">[{escape_text(ref_id)}] {escape_text(ref_loc)}</span>'
                                    f'<div>{escape_text(excerpt)}</div></div>',
                                    unsafe_allow_html=True,
                                )
                            for g_item in graph_rels[:5]:
                                if not isinstance(g_item, dict):
                                    continue
                                subj = g_item.get("subject") or g_item.get("source")
                                obj = g_item.get("object") or g_item.get("target")
                                rel_nm = str(g_item.get("relation") or "").replace("_", " ")
                                st.markdown(
                                    f'<div class="kg-citation-card"><strong>{escape_text(subj)}</strong> '
                                    f'<span class="kg-citation-ref">--{escape_text(rel_nm)}--></span> '
                                    f'<strong>{escape_text(obj)}</strong></div>',
                                    unsafe_allow_html=True,
                                )

            live_turn_slot = st.empty()

        # Fixed bottom inline input bar inside the unified bordered card
        st.markdown('<div class="kg-askme-input-sep"></div>', unsafe_allow_html=True)
        with st.form(f"sidebar_askme_form_{aid}", clear_on_submit=True, border=False):
            in_col_attach, in_col_txt, in_col_send = st.columns([0.62, 1.88, 1.1], gap="small", vertical_alignment="center")
            with in_col_attach:
                attach_clicked = st.form_submit_button(
                    "📎",
                    help="Upload or attach a PDF document in Analyze Document",
                    use_container_width=True,
                    disabled=is_streaming,
                )
            with in_col_txt:
                prompt_val = st.text_input(
                    "Ask a question",
                    placeholder="Ask something...",
                    label_visibility="collapsed",
                    key=f"sidebar_askme_input_{aid}",
                    disabled=is_streaming,
                )
            with in_col_send:
                submitted = st.form_submit_button(
                    "Send",
                    type="primary",
                    use_container_width=True,
                    disabled=(not backend_ok) or is_streaming,
                )

        clear_clicked = False
        if history:
            if st.button(
                "Clear Conversation",
                key=f"sidebar_askme_clear_{aid}",
                use_container_width=True,
                disabled=is_streaming,
            ):
                clear_clicked = True

        if attach_clicked:
            on_attach_pdf()
            return
        if clear_clicked and history:
            del_res = api_client.delete(f"/api/analyses/{aid}/chat")
            if del_res.ok:
                st.rerun()
            else:
                render_error_panel("Clear Chat Failed", del_res.error or "Unable to clear history.")
        elif submitted and prompt_val.strip() and not is_streaming:
            question_clean = prompt_val.strip()
            turn_num = len(history) + 1
            st.session_state[inflight_key] = True
            completed_ok = False
            stream_error: Optional[str] = None
            partial_chunks: List[str] = []

            if empty_notice is not None:
                empty_notice.empty()

            live_turn_slot.markdown(
                _live_turn_html(
                    turn_num,
                    question_clean,
                    "Retrieving passages and preparing grounded context...",
                    "THINKING",
                    streaming_cursor=True,
                ),
                unsafe_allow_html=True,
            )

            try:
                if hasattr(api_client, "stream_post"):
                    last_paint = 0.0
                    fallback_sync = False
                    for event in api_client.stream_post(
                        f"/api/analyses/{aid}/ask/stream",
                        json_body={"question": question_clean},
                        timeout=180,
                    ):
                        etype = event.get("type")
                        if etype == "meta":
                            if not partial_chunks:
                                p_cnt = len(event.get("citations") or [])
                                live_turn_slot.markdown(
                                    _live_turn_html(
                                        turn_num,
                                        question_clean,
                                        f"Found {p_cnt} passage(s). Generating grounded response...",
                                        "THINKING",
                                        streaming_cursor=True,
                                    ),
                                    unsafe_allow_html=True,
                                )
                        elif etype == "token":
                            tok = str(event.get("content") or "")
                            if tok:
                                is_first = not partial_chunks
                                partial_chunks.append(tok)
                                now = time.perf_counter()
                                if is_first or (now - last_paint) >= 0.05:
                                    last_paint = now
                                    live_turn_slot.markdown(
                                        _live_turn_html(
                                            turn_num,
                                            question_clean,
                                            "".join(partial_chunks),
                                            "STREAMING",
                                            streaming_cursor=True,
                                        ),
                                        unsafe_allow_html=True,
                                    )
                        elif etype == "done":
                            final_turn = event.get("turn")
                            if isinstance(final_turn, dict):
                                mode_lbl = str(final_turn.get("generation_mode") or "evidence").replace("_", " ").upper()
                                live_turn_slot.markdown(
                                    _live_turn_html(
                                        turn_num,
                                        question_clean,
                                        str(final_turn.get("answer") or "".join(partial_chunks)),
                                        mode_lbl,
                                        streaming_cursor=False,
                                    ),
                                    unsafe_allow_html=True,
                                )
                            completed_ok = True
                            break
                        elif etype == "error":
                            if event.get("status_code") == 404 and not partial_chunks:
                                fallback_sync = True
                                break
                            stream_error = str(event.get("detail") or "Unable to answer question.")
                            break

                    if fallback_sync:
                        ask_res = api_client.post(
                            f"/api/analyses/{aid}/ask",
                            json_body={"question": question_clean},
                            timeout=180,
                        )
                        completed_ok = bool(ask_res.ok)
                        if not ask_res.ok:
                            stream_error = ask_res.error or "Unable to answer question."
                    elif not completed_ok and not stream_error:
                        stream_error = "Stream ended unexpectedly before completion."
                else:
                    ask_res = api_client.post(
                        f"/api/analyses/{aid}/ask",
                        json_body={"question": question_clean},
                        timeout=180,
                    )
                    completed_ok = bool(ask_res.ok)
                    if not ask_res.ok:
                        stream_error = ask_res.error or "Unable to answer question."
            finally:
                st.session_state[inflight_key] = False

            if completed_ok:
                st.rerun()
            else:
                if partial_chunks:
                    live_turn_slot.markdown(
                        _live_turn_html(
                            turn_num,
                            question_clean,
                            "".join(partial_chunks),
                            "PARTIAL",
                            streaming_cursor=False,
                        ),
                        unsafe_allow_html=True,
                    )
                render_error_panel("Assistant Error", stream_error or "Unable to answer question.")


def render_system_status(
    health_data: Optional[Dict[str, Any]],
    *,
    backend_ok: bool,
    theme_name: str | None = None,
) -> None:
    """Render compact service health footer anchored at the bottom of the sidebar."""
    t = get_tokens(theme_name)
    api_dot = t["success"] if backend_ok else t["error"]
    api_txt = "API Online" if backend_ok else "API Offline"

    neo4j_ok = bool(isinstance(health_data, dict) and health_data.get("neo4j_available"))
    neo4j_txt = "Neo4j: Online" if neo4j_ok else "Neo4j: Fallback"

    sem_ok = bool(isinstance(health_data, dict) and health_data.get("semantic_indexed"))
    sem_txt = "FAISS: Indexed" if sem_ok else "FAISS: Standby"

    st.markdown(
        f"""
        <div class="kg-sidebar-status-footer">
            <div class="kg-status-line">
                <span style="font-weight:600; letter-spacing:0.08em;">SYSTEM STATUS</span>
                <span style="color:{t['text_primary']}; display:inline-flex; align-items:center; gap:0.35rem;">
                    <span class="kg-badge-dot" style="background-color:{api_dot};"></span>{api_txt}
                </span>
            </div>
            <div class="kg-status-line" style="font-size:0.64rem; opacity:0.85;">
                <span>{neo4j_txt}</span>
                <span>{sem_txt}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_resizer_controller() -> None:
    """Attach bounded horizontal sidebar sliding and vertical Ask Me chatbot sliding."""
    import streamlit.components.v1 as components

    components.html(
        """
        <script>
        (function() {
            const pWin = window.parent;
            const pDoc = pWin.document;
            const SIDEBAR_KEY = 'kgai_sidebar_width_px';
            const ASKME_KEY = 'kgai_askme_height_px';
            const MIN_W = 270;
            const MIN_ASKME_H = 200;

            function maxWidthForViewport() {
                const vw = pWin.innerWidth || 1440;
                return Math.min(480, Math.max(340, Math.round(vw * 0.40)));
            }

            function maxAskmeHeightForViewport() {
                const vh = pWin.innerHeight || 900;
                return Math.max(320, Math.round(vh - 150));
            }

            function clamp(val, lo, hi) {
                return Math.max(lo, Math.min(hi, val));
            }

            function notifyPlotly() {
                if (!pWin.Plotly || !pWin.Plotly.Plots) return;
                pDoc.querySelectorAll('.js-plotly-plot').forEach((node) => {
                    try { pWin.Plotly.Plots.resize(node); } catch (_) {}
                });
            }

            function applyWidth(px, persist) {
                if ((pWin.innerWidth || 1440) <= 960) return;
                const clamped = clamp(Math.round(px), MIN_W, maxWidthForViewport());
                pDoc.documentElement.style.setProperty('--kg-sidebar-w', clamped + 'px');
                if (persist) {
                    try { pWin.localStorage.setItem(SIDEBAR_KEY, String(clamped)); } catch (_) {}
                }
                pWin.requestAnimationFrame(notifyPlotly);
            }

            function applyAskmeHeight(px, persist) {
                if ((pWin.innerWidth || 1440) <= 960) return;
                const clamped = clamp(Math.round(px), MIN_ASKME_H, maxAskmeHeightForViewport());
                pDoc.documentElement.style.setProperty('--kg-askme-h', clamped + 'px');
                if (persist) {
                    try { pWin.localStorage.setItem(ASKME_KEY, String(clamped)); } catch (_) {}
                }
            }

            function restoreSavedGeometry() {
                if ((pWin.innerWidth || 1440) <= 960) {
                    pDoc.documentElement.style.removeProperty('--kg-sidebar-w');
                    pDoc.documentElement.style.removeProperty('--kg-askme-h');
                    return;
                }
                try {
                    const savedW = parseFloat(pWin.localStorage.getItem(SIDEBAR_KEY));
                    if (!Number.isNaN(savedW) && savedW >= MIN_W) {
                        applyWidth(savedW, false);
                    }
                    const savedH = parseFloat(pWin.localStorage.getItem(ASKME_KEY));
                    if (!Number.isNaN(savedH) && savedH >= MIN_ASKME_H) {
                        applyAskmeHeight(savedH, false);
                    }
                } catch (_) {}
            }

            function mountHandles() {
                const appView = pDoc.querySelector('[data-testid="stAppViewContainer"]');
                const sb = pDoc.querySelector('[data-testid="stColumn"]:has(#kg-left-sidebar-anchor)');
                if (!appView || !sb) return false;

                restoreSavedGeometry();

                // 1. Horizontal sidebar slide handle
                let sbHandle = appView.querySelector(':scope > .kg-sidebar-resizer');
                if (!sbHandle) {
                    sbHandle = pDoc.createElement('div');
                    sbHandle.className = 'kg-sidebar-resizer';
                    sbHandle.setAttribute('role', 'separator');
                    sbHandle.setAttribute('aria-orientation', 'vertical');
                    sbHandle.setAttribute('aria-label', 'Slide sidebar horizontally (double-click to reset)');
                    sbHandle.title = 'Drag to slide sidebar width (double-click to reset)';
                    appView.appendChild(sbHandle);
                }

                if (!sbHandle.dataset.kgBound) {
                    sbHandle.dataset.kgBound = '1';
                    let draggingW = false;

                    function onMoveW(ev) {
                        if (!draggingW) return;
                        applyWidth(ev.clientX, false);
                    }

                    function stopDragW(ev) {
                        if (!draggingW) return;
                        draggingW = false;
                        sbHandle.classList.remove('kg-dragging');
                        pDoc.documentElement.classList.remove('kg-sidebar-resizing');
                        pDoc.body.style.userSelect = '';
                        pDoc.body.style.cursor = '';
                        if (ev && typeof ev.clientX === 'number') {
                            applyWidth(ev.clientX, true);
                        }
                        pWin.removeEventListener('pointermove', onMoveW, true);
                        pWin.removeEventListener('pointerup', stopDragW, true);
                        pWin.removeEventListener('mousemove', onMoveW, true);
                        pWin.removeEventListener('mouseup', stopDragW, true);
                        setTimeout(notifyPlotly, 60);
                    }

                    function startDragW(ev) {
                        if ((pWin.innerWidth || 1440) <= 960) return;
                        ev.preventDefault();
                        draggingW = true;
                        sbHandle.classList.add('kg-dragging');
                        pDoc.documentElement.classList.add('kg-sidebar-resizing');
                        pDoc.body.style.userSelect = 'none';
                        pDoc.body.style.cursor = 'col-resize';
                        pWin.addEventListener('pointermove', onMoveW, true);
                        pWin.addEventListener('pointerup', stopDragW, true);
                        pWin.addEventListener('mousemove', onMoveW, true);
                        pWin.addEventListener('mouseup', stopDragW, true);
                    }

                    sbHandle.addEventListener('pointerdown', startDragW);
                    sbHandle.addEventListener('mousedown', startDragW);
                    sbHandle.addEventListener('dblclick', () => {
                        try { pWin.localStorage.removeItem(SIDEBAR_KEY); } catch (_) {}
                        pDoc.documentElement.style.removeProperty('--kg-sidebar-w');
                        pWin.requestAnimationFrame(notifyPlotly);
                    });
                }

                // 2. Vertical chatbot slide handle along top edge of Ask Me card
                const card = sb.querySelector('.st-key-askme_card');
                if (card) {
                    let chatHandle = card.querySelector(':scope > .kg-askme-resizer');
                    if (!chatHandle) {
                        chatHandle = pDoc.createElement('div');
                        chatHandle.className = 'kg-askme-resizer';
                        chatHandle.setAttribute('role', 'separator');
                        chatHandle.setAttribute('aria-orientation', 'horizontal');
                        chatHandle.setAttribute('aria-label', 'Slide chatbot vertically (double-click to reset)');
                        chatHandle.title = 'Drag to slide chatbot height (double-click to reset)';
                        card.appendChild(chatHandle);
                    }

                    if (!chatHandle.dataset.kgBound) {
                        chatHandle.dataset.kgBound = '1';
                        let draggingH = false;
                        let anchorBottom = 0;

                        function onMoveH(ev) {
                            if (!draggingH) return;
                            applyAskmeHeight(anchorBottom - ev.clientY, false);
                        }

                        function stopDragH(ev) {
                            if (!draggingH) return;
                            draggingH = false;
                            chatHandle.classList.remove('kg-dragging');
                            pDoc.documentElement.classList.remove('kg-askme-resizing');
                            pDoc.body.style.userSelect = '';
                            pDoc.body.style.cursor = '';
                            if (ev && typeof ev.clientY === 'number') {
                                applyAskmeHeight(anchorBottom - ev.clientY, true);
                            }
                            pWin.removeEventListener('pointermove', onMoveH, true);
                            pWin.removeEventListener('pointerup', stopDragH, true);
                            pWin.removeEventListener('mousemove', onMoveH, true);
                            pWin.removeEventListener('mouseup', stopDragH, true);
                        }

                        function startDragH(ev) {
                            if ((pWin.innerWidth || 1440) <= 960) return;
                            ev.preventDefault();
                            ev.stopPropagation();
                            draggingH = true;
                            anchorBottom = card.getBoundingClientRect().bottom;
                            chatHandle.classList.add('kg-dragging');
                            pDoc.documentElement.classList.add('kg-askme-resizing');
                            pDoc.body.style.userSelect = 'none';
                            pDoc.body.style.cursor = 'row-resize';
                            pWin.addEventListener('pointermove', onMoveH, true);
                            pWin.addEventListener('pointerup', stopDragH, true);
                            pWin.addEventListener('mousemove', onMoveH, true);
                            pWin.addEventListener('mouseup', stopDragH, true);
                        }

                        chatHandle.addEventListener('pointerdown', startDragH);
                        chatHandle.addEventListener('mousedown', startDragH);
                        chatHandle.addEventListener('dblclick', (ev) => {
                            ev.stopPropagation();
                            try { pWin.localStorage.removeItem(ASKME_KEY); } catch (_) {}
                            pDoc.documentElement.style.removeProperty('--kg-askme-h');
                        });
                    }
                }
                return true;
            }

            if (!mountHandles()) {
                let tries = 0;
                const timer = pWin.setInterval(() => {
                    tries += 1;
                    if (mountHandles() || tries > 30) {
                        pWin.clearInterval(timer);
                    }
                }, 80);
            }
            if (!pWin.__kgSidebarResizeHooked) {
                pWin.__kgSidebarResizeHooked = true;
                pWin.addEventListener('resize', restoreSavedGeometry);
            }
        })();
        </script>
        """,
        height=0,
    )

