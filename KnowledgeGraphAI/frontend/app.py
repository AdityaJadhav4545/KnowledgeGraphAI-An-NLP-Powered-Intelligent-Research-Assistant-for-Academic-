"""KnowledgeGraphAI — Industrial / Architectural AI-Powered Knowledge Graph Research Assistant."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import streamlit as st

# Ensure parent of KnowledgeGraphAI is importable when launched from workspace root
_PACKAGE_PARENT = str(Path(__file__).resolve().parents[2])
if _PACKAGE_PARENT not in sys.path:
    sys.path.insert(0, _PACKAGE_PARENT)

from KnowledgeGraphAI.frontend.components.api_client import APIClient
from KnowledgeGraphAI.frontend.components.theme import (
    escape_text,
    init_sidebar_state,
    init_split_ratio,
    init_theme,
    inject_theme_css,
    set_sidebar_collapsed,
)
from KnowledgeGraphAI.frontend.components.ui import (
    render_boxed_ask_me,
    render_collapsed_sidebar_bar,
    render_error_panel,
    render_sidebar_brand_header,
    render_sidebar_resizer_controller,
    render_status_badge,
    render_system_status,
)
from KnowledgeGraphAI.frontend.views import analyze, explore, report

NAV_ITEMS = [
    "Analyze Document",
    "Explore Knowledge",
    "Generate Report",
]


def _get_api_client() -> APIClient:
    base_url = os.getenv("KNOWLEDGEGRAPHAI_API_URL") or os.getenv("BACKEND_URL") or "http://127.0.0.1:8000"
    api_key = os.getenv("API_KEY") or None
    return APIClient(base_url=base_url, api_key=api_key)


def _navigate_to(section: str) -> None:
    if section in NAV_ITEMS:
        st.session_state["active_nav"] = section
        st.query_params["nav"] = section
        st.session_state["_pending_nav"] = section
        st.rerun()


def _attach_pdf_navigate() -> None:
    st.session_state["active_nav"] = "Analyze Document"
    st.query_params["nav"] = "Analyze Document"
    st.session_state["_pending_nav"] = "Analyze Document"
    st.session_state["reset_analyze_inputs"] = True
    st.rerun()


def _format_doc_option(item: Dict[str, Any]) -> str:
    src = "PDF" if item.get("source_type") == "pdf" else "TXT"
    title = str(item.get("title") or "Untitled Document").strip()
    if len(title) > 32:
        title = title[:29] + "..."
    ents = item.get("entity_count", 0)
    rels = item.get("relationship_count", 0)
    return f"[{src}] {title} ({ents}E / {rels}R)"


def _render_sidebar_panel(
    *,
    api_client: APIClient,
    active_theme: str,
    t: Dict[str, str],
    analyses: List[Dict[str, Any]],
    available_ids: List[str],
    active_detail: Optional[Dict[str, Any]],
    health_data: Optional[Dict[str, Any]],
    backend_ok: bool,
) -> str:
    st.markdown('<div id="kg-left-sidebar-anchor"></div>', unsafe_allow_html=True)

    # A. Brand Header + Collapse Control
    render_sidebar_brand_header(
        active_theme,
        on_collapse=lambda: set_sidebar_collapsed(True),
    )

    # B & C. Workspace Navigation + Your Documents (scrolls gracefully if Ask Me slides upward)
    with st.container(border=False, key="sidebar_top_nav"):
        st.markdown('<div class="kg-sidebar-section-label kg-workspace-heading">Workspace</div>', unsafe_allow_html=True)
        nav_choice = st.radio(
            "Workspace Navigation",
            NAV_ITEMS,
            key="nav_section",
            label_visibility="collapsed",
        )
        if nav_choice in NAV_ITEMS:
            st.session_state["active_nav"] = nav_choice
            st.query_params["nav"] = nav_choice

        st.markdown('<div class="kg-sidebar-section-label">Your Documents</div>', unsafe_allow_html=True)
        if st.button("+ New Analysis", key="sidebar_new_analysis_btn", type="primary", use_container_width=True):
            _attach_pdf_navigate()

        if analyses:
            by_id = {item["analysis_id"]: item for item in analyses if item.get("analysis_id")}
            selected_sidebar_id = st.selectbox(
                "Analyzed Documents",
                options=available_ids,
                key="selected_analysis_id",
                format_func=lambda aid: _format_doc_option(by_id.get(aid, {})),
                label_visibility="collapsed",
            )
            if selected_sidebar_id:
                st.session_state["active_analysis_id"] = selected_sidebar_id
                st.query_params["doc"] = selected_sidebar_id
            selected_summary = by_id.get(selected_sidebar_id or "", {})
            if selected_summary:
                src_label = "PDF Document" if selected_summary.get("source_type") == "pdf" else "Pasted Text"
                status_html = render_status_badge(str(selected_summary.get("status") or "completed"), active_theme)
                title_html = escape_text(selected_summary.get("title") or "Untitled Document")
                st.markdown(
                    f"""
                    <div class="kg-card-elevated kg-sidebar-doc-card" style="margin-top:0.1rem; margin-bottom:0.14rem; padding:0.4rem 0.6rem;">
                        <div style="display:flex; justify-content:space-between; align-items:center; gap:0.4rem; margin-bottom:0.2rem;">
                            <span class="kg-mono" style="font-size:0.64rem; color:{t['text_secondary']};">{src_label.upper()}</span>
                            {status_html}
                        </div>
                        <div style="font-size:0.8rem; font-weight:600; color:{t['text_primary']}; line-height:1.25; margin-bottom:0.2rem;">
                            {title_html}
                        </div>
                        <div class="kg-mono" style="font-size:0.68rem; color:{t['text_secondary']};">
                            {selected_summary.get('entity_count', 0)} entities &middot; {selected_summary.get('relationship_count', 0)} relations
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                f"""
                <div class="kg-card-elevated" style="padding:0.65rem 0.72rem; margin:0.35rem 0 0.65rem 0;">
                    <div style="font-size:0.78rem; color:{t['text_secondary']};">
                        No analyzed documents yet. Upload a PDF or paste text to begin.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # D. Ask Me — Boxed AI Assistant in Lower Sidebar
    render_boxed_ask_me(
        api_client,
        active_detail,
        backend_ok=backend_ok,
        on_attach_pdf=_attach_pdf_navigate,
        theme_name=active_theme,
    )

    # E. System Status Anchored at Bottom
    render_system_status(
        health_data,
        backend_ok=backend_ok,
        theme_name=active_theme,
    )
    render_sidebar_resizer_controller()
    return str(nav_choice or "Analyze Document")


def _render_main_workspace(
    *,
    nav_choice: str,
    api_client: APIClient,
    analyses_res: Any,
    active_detail: Optional[Dict[str, Any]],
    sidebar_collapsed: bool,
    active_theme: str,
) -> None:
    st.markdown('<div id="kg-main-workspace-anchor"></div>', unsafe_allow_html=True)

    if sidebar_collapsed:
        render_collapsed_sidebar_bar(
            active_theme,
            active_detail,
            on_expand=lambda: set_sidebar_collapsed(False),
        )

    if not analyses_res.ok and analyses_res.error:
        render_error_panel(
            "Backend API Unavailable",
            f"Unable to reach FastAPI service ({analyses_res.error}). Start the backend server or verify KNOWLEDGEGRAPHAI_API_URL.",
        )

    if nav_choice == "Analyze Document":
        analyze.render(api_client, on_navigate=_navigate_to, active_doc=active_detail)
    elif nav_choice == "Explore Knowledge":
        explore.render(api_client, active_detail, on_navigate=_navigate_to)
    else:
        report.render(api_client, active_detail, on_navigate=_navigate_to)


def main() -> None:
    st.set_page_config(
        page_title="KnowledgeGraphAI — Research Workspace",
        page_icon="◈",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    active_theme = init_theme()
    t = inject_theme_css(active_theme)
    sidebar_collapsed = init_sidebar_state()
    init_split_ratio()

    # Resolve persistent navigation (independent of sidebar collapse widget lifecycle)
    if "_pending_nav" in st.session_state:
        resolved_nav = st.session_state.pop("_pending_nav")
    elif st.session_state.get("nav_section") in NAV_ITEMS:
        resolved_nav = str(st.session_state["nav_section"])
    elif st.session_state.get("active_nav") in NAV_ITEMS:
        resolved_nav = str(st.session_state["active_nav"])
    elif st.query_params.get("nav") in NAV_ITEMS:
        resolved_nav = str(st.query_params.get("nav"))
    else:
        resolved_nav = "Analyze Document"

    st.session_state["active_nav"] = resolved_nav
    st.session_state["nav_section"] = resolved_nav
    if st.query_params.get("nav") != resolved_nav:
        st.query_params["nav"] = resolved_nav

    api_client = _get_api_client()

    analyses_res = api_client.get("/api/analyses")
    analyses: List[Dict[str, Any]] = analyses_res.data if (analyses_res.ok and isinstance(analyses_res.data, list)) else []
    available_ids = [item["analysis_id"] for item in analyses if item.get("analysis_id")]

    if "_pending_selected_analysis_id" in st.session_state:
        cand_id = st.session_state.pop("_pending_selected_analysis_id")
    elif st.session_state.get("selected_analysis_id") in available_ids:
        cand_id = st.session_state["selected_analysis_id"]
    elif st.session_state.get("active_analysis_id") in available_ids:
        cand_id = st.session_state["active_analysis_id"]
    elif st.query_params.get("doc") in available_ids:
        cand_id = st.query_params.get("doc")
    else:
        cand_id = available_ids[0] if available_ids else None

    if cand_id not in available_ids:
        cand_id = available_ids[0] if available_ids else None

    st.session_state["active_analysis_id"] = cand_id
    st.session_state["selected_analysis_id"] = cand_id
    if cand_id and st.query_params.get("doc") != cand_id:
        st.query_params["doc"] = cand_id

    active_detail: Optional[Dict[str, Any]] = None
    if cand_id:
        detail_res = api_client.get(f"/api/analyses/{cand_id}")
        if detail_res.ok and isinstance(detail_res.data, dict):
            active_detail = detail_res.data

    health_res = api_client.get("/health")
    health_data = health_res.data if (health_res.ok and isinstance(health_res.data, dict)) else None
    backend_ok = bool(health_data and health_data.get("status") == "ok")

    if not sidebar_collapsed:
        sidebar_col, main_col = st.columns([1.0, 3.0], gap="medium")
        with sidebar_col:
            nav_choice = _render_sidebar_panel(
                api_client=api_client,
                active_theme=active_theme,
                t=t,
                analyses=analyses,
                available_ids=available_ids,
                active_detail=active_detail,
                health_data=health_data,
                backend_ok=backend_ok,
            )
        with main_col:
            _render_main_workspace(
                nav_choice=nav_choice,
                api_client=api_client,
                analyses_res=analyses_res,
                active_detail=active_detail,
                sidebar_collapsed=False,
                active_theme=active_theme,
            )
    else:
        _render_main_workspace(
            nav_choice=resolved_nav,
            api_client=api_client,
            analyses_res=analyses_res,
            active_detail=active_detail,
            sidebar_collapsed=True,
            active_theme=active_theme,
        )


if __name__ == "__main__":
    main()
