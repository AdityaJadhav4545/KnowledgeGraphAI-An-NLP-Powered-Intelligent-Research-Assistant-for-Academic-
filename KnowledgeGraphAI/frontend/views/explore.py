"""Explore Knowledge view — Resizable Knowledge Graph + Document Insights workspace."""

from __future__ import annotations

import json
from typing import Any, Callable, Dict, List, Optional

import streamlit as st
import streamlit.components.v1 as components

from KnowledgeGraphAI.frontend.components.api_client import APIClient
from KnowledgeGraphAI.frontend.components.graph_view import (
    build_interactive_figure,
    filter_subgraph,
)
from KnowledgeGraphAI.frontend.components.theme import (
    MAX_SPLIT_PCT,
    MIN_SPLIT_PCT,
    escape_text,
    get_entity_color,
    get_tokens,
    init_split_ratio,
    init_theme,
    toggle_theme,
)
from KnowledgeGraphAI.frontend.components.ui import (
    render_empty_state,
    render_entity_badge,
    render_global_header,
    render_metric_cards,
    render_section_heading,
    render_status_badge,
)


def _inject_resizable_split_controller(initial_pct: float) -> None:
    """Attach a real draggable vertical divider between Knowledge Graph and Document Insights."""
    config_json = json.dumps(
        {
            "initialPct": round(float(initial_pct), 2),
            "minPct": float(MIN_SPLIT_PCT),
            "maxPct": float(MAX_SPLIT_PCT),
            "storageKey": "kgai_explore_split_pct",
        }
    )
    html_code = f"""
    <script>
    (function() {{
        const cfg = {config_json};
        let pDoc, pWin;
        try {{
            pWin = window.parent;
            pDoc = pWin.document;
        }} catch (e) {{
            return;
        }}
        if (!pDoc || !pDoc.body) return;

        function clamp(val, lo, hi) {{
            return Math.max(lo, Math.min(hi, val));
        }}

        function resizePlotlyIn(el) {{
            try {{
                if (!pWin.Plotly || !el) return;
                const plots = el.querySelectorAll('.js-plotly-plot');
                plots.forEach((gd) => {{
                    try {{ pWin.Plotly.Plots.resize(gd); }} catch (_) {{}}
                }});
            }} catch (_) {{}}
        }}

        function initSplit() {{
            const leftAnchor = pDoc.getElementById('kg-split-left-anchor');
            const rightAnchor = pDoc.getElementById('kg-split-right-anchor');
            if (!leftAnchor || !rightAnchor) return false;

            const leftCol = leftAnchor.closest('[data-testid="stColumn"]');
            const rightCol = rightAnchor.closest('[data-testid="stColumn"]');
            if (!leftCol || !rightCol) return false;
            const block = leftCol.parentElement;
            if (!block) return false;

            let handle = block.querySelector(':scope > .kg-split-resizer');
            if (!handle) {{
                handle = pDoc.createElement('div');
                handle.className = 'kg-split-resizer';
                handle.setAttribute('role', 'separator');
                handle.setAttribute('aria-orientation', 'vertical');
                handle.setAttribute('title', 'Drag left or right to resize Knowledge Graph and Document Insights');
                block.insertBefore(handle, rightCol);
            }}

            function readSavedPct() {{
                try {{
                    const urlVal = new URLSearchParams(pWin.location.search).get('split');
                    const lsVal = pWin.localStorage.getItem(cfg.storageKey);
                    const candidate = parseFloat(lsVal || urlVal || cfg.initialPct);
                    if (!Number.isNaN(candidate)) {{
                        return clamp(candidate, cfg.minPct, cfg.maxPct);
                    }}
                }} catch (_) {{}}
                return clamp(cfg.initialPct, cfg.minPct, cfg.maxPct);
            }}

            function boundsForWidth(totalW) {{
                if (!totalW || totalW <= 0) return [cfg.minPct, cfg.maxPct];
                const minLeft = Math.max(cfg.minPct, (420 / totalW) * 100);
                const maxLeft = Math.min(cfg.maxPct, 100 - (300 / totalW) * 100);
                if (minLeft > maxLeft) return [50, 50];
                return [minLeft, maxLeft];
            }}

            function applyPct(pct, persist) {{
                const blockRect = block.getBoundingClientRect();
                const shouldStack = (pWin.innerWidth <= 960) || (blockRect.width > 0 && blockRect.width < 740);
                if (shouldStack) {{
                    block.classList.add('kg-split-stacked');
                    block.style.removeProperty('flex-wrap');
                    ['flex', 'max-width', 'width'].forEach((prop) => {{
                        leftCol.style.removeProperty(prop);
                        rightCol.style.removeProperty(prop);
                    }});
                    pWin.requestAnimationFrame(() => resizePlotlyIn(leftCol));
                    return;
                }}
                block.classList.remove('kg-split-stacked');
                block.style.setProperty('flex-wrap', 'nowrap', 'important');
                const [dynMin, dynMax] = boundsForWidth(blockRect.width);
                const clamped = clamp(pct, dynMin, dynMax);
                const handleW = 22;
                const leftExpr = 'calc(' + clamped.toFixed(2) + '% - ' + (handleW / 2) + 'px)';
                const rightPct = (100 - clamped).toFixed(2);
                const rightExpr = 'calc(' + rightPct + '% - ' + (handleW / 2) + 'px)';

                leftCol.style.setProperty('flex', '0 0 ' + leftExpr, 'important');
                leftCol.style.setProperty('max-width', leftExpr, 'important');
                leftCol.style.setProperty('width', leftExpr, 'important');

                rightCol.style.setProperty('flex', '0 0 ' + rightExpr, 'important');
                rightCol.style.setProperty('max-width', rightExpr, 'important');
                rightCol.style.setProperty('width', rightExpr, 'important');

                if (persist) {{
                    try {{
                        pWin.localStorage.setItem(cfg.storageKey, clamped.toFixed(1));
                        const url = new URL(pWin.location.href);
                        url.searchParams.set('split', clamped.toFixed(1));
                        pWin.history.replaceState({{}}, '', url.toString());
                    }} catch (_) {{}}
                }}
                pWin.requestAnimationFrame(() => resizePlotlyIn(leftCol));
            }}

            applyPct(readSavedPct(), false);

            if (!handle.dataset.kgBound) {{
                handle.dataset.kgBound = '1';
                let dragging = false;

                function onMove(ev) {{
                    if (!dragging) return;
                    const rect = block.getBoundingClientRect();
                    if (rect.width <= 0) return;
                    const pct = ((ev.clientX - rect.left) / rect.width) * 100;
                    applyPct(pct, false);
                }}

                function stopDrag(ev) {{
                    if (!dragging) return;
                    dragging = false;
                    handle.classList.remove('kg-dragging');
                    pDoc.body.style.userSelect = '';
                    pDoc.body.style.cursor = '';
                    const rect = block.getBoundingClientRect();
                    if (rect.width > 0 && ev && typeof ev.clientX === 'number') {{
                        const pct = ((ev.clientX - rect.left) / rect.width) * 100;
                        applyPct(pct, true);
                    }}
                    pWin.removeEventListener('pointermove', onMove, true);
                    pWin.removeEventListener('pointerup', stopDrag, true);
                    pWin.removeEventListener('mousemove', onMove, true);
                    pWin.removeEventListener('mouseup', stopDrag, true);
                    setTimeout(() => resizePlotlyIn(leftCol), 60);
                }}

                function startDrag(ev) {{
                    if (pWin.innerWidth <= 960 || block.classList.contains('kg-split-stacked')) return;
                    ev.preventDefault();
                    dragging = true;
                    handle.classList.add('kg-dragging');
                    pDoc.body.style.userSelect = 'none';
                    pDoc.body.style.cursor = 'col-resize';
                    pWin.addEventListener('pointermove', onMove, true);
                    pWin.addEventListener('pointerup', stopDrag, true);
                    pWin.addEventListener('mousemove', onMove, true);
                    pWin.addEventListener('mouseup', stopDrag, true);
                }}

                handle.addEventListener('pointerdown', startDrag);
                handle.addEventListener('mousedown', startDrag);
            }}

            if (!block.dataset.kgResizeObserved && typeof pWin.ResizeObserver === 'function') {{
                block.dataset.kgResizeObserved = '1';
                const ro = new pWin.ResizeObserver(() => {{
                    if (pWin.innerWidth <= 960) {{
                        applyPct(cfg.initialPct, false);
                    }} else {{
                        applyPct(readSavedPct(), false);
                    }}
                }});
                ro.observe(block);
            }}
            return true;
        }}

        let attempts = 0;
        const timer = setInterval(() => {{
            attempts += 1;
            if (initSplit() || attempts > 20) {{
                clearInterval(timer);
            }}
        }}, 80);
    }})();
    </script>
    """
    components.html(html_code, height=0)


def _render_graph_workspace(analysis: Dict[str, Any], theme_name: str) -> None:
    t = get_tokens(theme_name)
    aid = analysis["analysis_id"]
    graph_json = analysis.get("graph") or {"nodes": [], "edges": [], "stats": {}}
    all_nodes: List[Dict[str, Any]] = list(graph_json.get("nodes") or [])
    all_edges: List[Dict[str, Any]] = list(graph_json.get("edges") or [])

    st.markdown('<div id="kg-split-left-anchor"></div>', unsafe_allow_html=True)

    with st.container(border=True, key="kg_panel_card"):
        kg_icon = (
            f'<svg width="17" height="17" viewBox="0 0 24 24" fill="none">'
            f'<circle cx="12" cy="5" r="2.5" stroke="{t["accent"]}" stroke-width="1.6"/>'
            f'<circle cx="5" cy="18" r="2.5" stroke="{t["accent"]}" stroke-width="1.6"/>'
            f'<circle cx="19" cy="18" r="2.5" stroke="{t["accent"]}" stroke-width="1.6"/>'
            f'<path d="M10.5 7L6.5 16M13.5 7L17.5 16M7.5 18H16.5" stroke="{t["accent"]}" stroke-width="1.4"/>'
            f"</svg>"
        )
        st.markdown(
            f'<div class="kg-panel-hdr-row">'
            f'<div class="kg-panel-hdr-title">{kg_icon}<span>Knowledge Graph</span></div>'
            f'<span class="kg-mono" style="font-size:0.71rem; color:{t["text_secondary"]};">{len(all_nodes)}N &middot; {len(all_edges)}E</span>'
            f"</div>",
            unsafe_allow_html=True,
        )

        if not all_nodes:
            render_empty_state(
                "No Graph Entities Available",
                "This document did not yield structured entities. Review Document Insights or ask questions via Ask Me in the sidebar.",
                kicker="Knowledge Graph",
            )
            return

        node_by_id = {n["id"]: n for n in all_nodes if n.get("id")}
        categories = sorted({str(n.get("category") or "Concept") for n in all_nodes})
        focus_options = [""] + [n["id"] for n in sorted(all_nodes, key=lambda x: x.get("degree", 0), reverse=True)]

        pending_focus_key = f"_pending_focus_{aid}"
        if pending_focus_key in st.session_state:
            st.session_state[f"graph_focus_{aid}"] = st.session_state.pop(pending_focus_key)

        reset_flag_key = f"_reset_graph_controls_{aid}"
        if st.session_state.pop(reset_flag_key, False):
            st.session_state[f"graph_search_{aid}"] = ""
            st.session_state[f"graph_cats_{aid}"] = categories
            st.session_state[f"graph_focus_{aid}"] = ""
            st.session_state[f"graph_selected_node_{aid}"] = None

        # Control bar row 1: Search & Category filters
        ctrl1, ctrl2 = st.columns([1.15, 1.85], gap="small")
        with ctrl1:
            search_query = st.text_input(
                "Search Entity",
                key=f"graph_search_{aid}",
                placeholder="Search entity or alias...",
            )
        with ctrl2:
            selected_categories = st.multiselect(
                "Filter Categories",
                options=categories,
                default=categories,
                key=f"graph_cats_{aid}",
            )

        # Control bar row 2: Focus node, max nodes, Fit / Reset buttons
        ctrl3, ctrl4, ctrl5, ctrl6 = st.columns([1.55, 1.0, 0.72, 0.72], vertical_alignment="bottom", gap="small")
        with ctrl3:
            focus_node_id = st.selectbox(
                "Inspect Entity",
                options=focus_options,
                key=f"graph_focus_{aid}",
                format_func=lambda nid: "All visible entities" if not nid else f"{node_by_id[nid]['label']} ({node_by_id[nid]['category']})",
            )
        with ctrl4:
            slider_max = max(10, min(120, len(all_nodes)))
            default_cap = min(45, slider_max)
            max_nodes = st.slider(
                "Max Nodes",
                min_value=min(5, slider_max),
                max_value=slider_max,
                value=default_cap,
                key=f"graph_max_nodes_{aid}",
            )
        with ctrl5:
            if st.button("Fit", key=f"graph_fit_btn_{aid}", help="Fit graph to view", use_container_width=True):
                st.session_state[f"graph_rev_num_{aid}"] = int(st.session_state.get(f"graph_rev_num_{aid}", 0)) + 1
                st.session_state[f"graph_rev_{aid}"] = f"fit-{st.session_state[f'graph_rev_num_{aid}']}"
                st.rerun()
        with ctrl6:
            if st.button("Reset", key=f"graph_reset_btn_{aid}", help="Reset filters and layout", use_container_width=True):
                st.session_state[reset_flag_key] = True
                st.session_state[f"graph_rev_num_{aid}"] = int(st.session_state.get(f"graph_rev_num_{aid}", 0)) + 1
                st.session_state[f"graph_rev_{aid}"] = f"reset-{st.session_state[f'graph_rev_num_{aid}']}"
                st.rerun()

        filtered_nodes, filtered_edges = filter_subgraph(
            graph_json,
            selected_categories=selected_categories,
            focus_node_id=focus_node_id or None,
            search_query=search_query or None,
            max_nodes=max_nodes,
        )

        selected_node_id = focus_node_id or st.session_state.get(f"graph_selected_node_{aid}")
        visible_ids = {n["id"] for n in filtered_nodes}
        if selected_node_id not in visible_ids:
            selected_node_id = None

        rev_token = str(st.session_state.get(f"graph_rev_{aid}", f"init-{theme_name}"))
        fig, _ = build_interactive_figure(
            filtered_nodes,
            filtered_edges,
            selected_node_id=selected_node_id,
            theme_name=theme_name,
            view_revision=f"{rev_token}-{theme_name}",
        )

        chart_state = st.plotly_chart(
            fig,
            use_container_width=True,
            key=f"plotly_kg_{aid}_{theme_name}",
            on_select="rerun",
            selection_mode="points",
            config={
                "displayModeBar": True,
                "scrollZoom": True,
                "responsive": True,
                "displaylogo": False,
                "modeBarButtonsToRemove": ["lasso2d", "select2d", "autoScale2d"],
            },
        )

        if isinstance(chart_state, dict):
            points = ((chart_state.get("selection") or {}).get("points")) or []
            for pt in points:
                cd = pt.get("customdata")
                if isinstance(cd, dict) and cd.get("id") in node_by_id:
                    clicked_id = cd["id"]
                    if clicked_id != st.session_state.get(f"graph_selected_node_{aid}"):
                        st.session_state[f"graph_selected_node_{aid}"] = clicked_id
                        selected_node_id = clicked_id
                    break

        st.markdown(
            f"""
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.4rem; margin:-0.25rem 0 0.65rem 0;">
                <span class="kg-mono" style="font-size:0.72rem; color:{t['text_secondary']};">
                    SHOWING {len(filtered_nodes)} / {len(all_nodes)} ENTITIES &middot; {len(filtered_edges)} / {len(all_edges)} RELATIONS
                </span>
                <span class="kg-mono" style="font-size:0.71rem; color:{t['text_secondary']};">
                    Scroll zoom &middot; Drag pan &middot; Click node to inspect
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Contextual Entity Details Panel
        if selected_node_id and selected_node_id in node_by_id:
            node = node_by_id[selected_node_id]
            outgoing = [e for e in all_edges if e.get("source") == selected_node_id]
            incoming = [e for e in all_edges if e.get("target") == selected_node_id]
            connected_ids = list(
                dict.fromkeys(
                    [e["target"] for e in outgoing if e.get("target") in node_by_id]
                    + [e["source"] for e in incoming if e.get("source") in node_by_id]
                )
            )
            aliases = ", ".join(node.get("aliases") or []) or "None recorded"
            source_refs = ", ".join(node.get("source_refs") or []) or "Document body"
            sample_context = node.get("sample_context") or "Extracted entity from document text; no separate definition passage is attached."
            cat = str(node.get("category") or "Concept")
            cat_color = get_entity_color(cat, theme_name)

            head_col, clear_sel_col = st.columns([4.0, 1.15], vertical_alignment="center")
            with head_col:
                render_section_heading("Entity Inspector", str(node.get("label") or selected_node_id))
            with clear_sel_col:
                if st.button("Clear Selection", key=f"clear_node_sel_{aid}", use_container_width=True):
                    st.session_state[f"graph_selected_node_{aid}"] = None
                    st.session_state[pending_focus_key] = ""
                    st.rerun()

            st.markdown(
                f"""
                <div class="kg-card-elevated" style="border-left:3px solid {cat_color};">
                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem; margin-bottom:0.45rem;">
                        {render_entity_badge(str(node.get('label') or ''), cat, theme_name)}
                        <span class="kg-mono" style="font-size:0.72rem; color:{t['text_secondary']};">
                            {escape_text(cat.upper())} &middot; DEG {node.get('degree', 0)} &middot; MENTIONS {node.get('occurrences', 1)} &middot; CONF {float(node.get('confidence') or 0.0):.2f}
                        </span>
                    </div>
                    <div style="font-size:0.84rem; color:{t['text_primary']}; line-height:1.48; margin-bottom:0.45rem;">
                        {escape_text(sample_context)}
                    </div>
                    <div class="kg-mono" style="font-size:0.72rem; color:{t['text_secondary']};">
                        ALIASES: {escape_text(aliases)} &nbsp;|&nbsp; SOURCE REFS: {escape_text(source_refs)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if connected_ids:
                st.markdown(
                    f'<div class="kg-section-kicker" style="margin-top:0.2rem;">Connected Entities ({len(connected_ids)})</div>',
                    unsafe_allow_html=True,
                )
                pill_cols = st.columns(min(4, len(connected_ids)))
                for idx, cid in enumerate(connected_ids[:8]):
                    neighbor = node_by_id[cid]
                    with pill_cols[idx % len(pill_cols)]:
                        if st.button(
                            f"{neighbor['label']}",
                            key=f"hop_entity_{aid}_{cid}_{idx}",
                            use_container_width=True,
                            help=f"Focus on {neighbor['label']} ({neighbor['category']})",
                        ):
                            st.session_state[pending_focus_key] = cid
                            st.session_state[f"graph_selected_node_{aid}"] = cid
                            st.rerun()

            def _format_edge_cards(edge_list: List[Dict[str, Any]], *, outgoing_dir: bool) -> str:
                parts: List[str] = []
                for edge in edge_list[:6]:
                    rel_txt = escape_text(str(edge.get("relation") or "").replace("_", " "))
                    src_ref = escape_text(edge.get("source_ref") or f"Page {edge.get('page_number', '?')}")
                    conf_val = float(edge.get("confidence") or 0.0)
                    if outgoing_dir:
                        peer = escape_text(edge.get("target_label") or edge.get("target"))
                        head = f'<span class="kg-citation-ref">{rel_txt}</span> -> <strong>{peer}</strong>'
                    else:
                        peer = escape_text(edge.get("source_label") or edge.get("source"))
                        head = f'<strong>{peer}</strong> <span class="kg-citation-ref">{rel_txt}</span> ->'
                    parts.append(
                        f'<div class="kg-citation-card">{head}'
                        f'<div class="kg-mono" style="font-size:0.7rem; color:{t["text_secondary"]}; margin-top:0.15rem;">'
                        f"Source: {src_ref} &middot; Conf {conf_val:.2f}</div></div>"
                    )
                return "".join(parts)

            rel_col_out, rel_col_in = st.columns(2, gap="small")
            with rel_col_out:
                st.markdown(
                    f'<div class="kg-section-kicker" style="margin-top:0.35rem;">Outgoing ({len(outgoing)})</div>',
                    unsafe_allow_html=True,
                )
                if outgoing:
                    st.markdown(_format_edge_cards(outgoing, outgoing_dir=True), unsafe_allow_html=True)
                else:
                    st.markdown('<div class="kg-muted">No outgoing edges.</div>', unsafe_allow_html=True)

            with rel_col_in:
                st.markdown(
                    f'<div class="kg-section-kicker" style="margin-top:0.35rem;">Incoming ({len(incoming)})</div>',
                    unsafe_allow_html=True,
                )
                if incoming:
                    st.markdown(_format_edge_cards(incoming, outgoing_dir=False), unsafe_allow_html=True)
                else:
                    st.markdown('<div class="kg-muted">No incoming edges.</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                """
                <div class="kg-card-elevated" style="padding:0.65rem 0.85rem; margin-bottom:0;">
                    <div class="kg-section-kicker">Entity Details</div>
                    <div class="kg-muted" style="font-size:0.82rem;">
                        Click any node in the graph or choose an item from <strong>Inspect Entity</strong> to view aliases, connections, and passage evidence.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _derive_document_summary(analysis: Dict[str, Any]) -> str:
    report = analysis.get("report")
    if isinstance(report, dict) and report.get("executive_summary"):
        return str(report["executive_summary"]).strip()
    passages = list(analysis.get("passages") or [])
    if passages:
        snippets = [str(p.get("text") or "").strip() for p in passages[:2] if str(p.get("text") or "").strip()]
        joined = " ".join(snippets)
        if joined:
            return (joined[:460] + "...") if len(joined) > 460 else joined
    return (
        f"Indexed {analysis.get('passage_count', 0)} passage(s) with "
        f"{analysis.get('entity_count', 0)} entities and {analysis.get('relationship_count', 0)} relationships."
    )


def _render_document_insights(
    analysis: Dict[str, Any],
    theme_name: str,
    on_navigate: Optional[Callable[[str], None]],
) -> None:
    t = get_tokens(theme_name)
    aid = analysis["analysis_id"]
    nodes: List[Dict[str, Any]] = list((analysis.get("graph") or {}).get("nodes") or analysis.get("entities") or [])
    edges: List[Dict[str, Any]] = list((analysis.get("graph") or {}).get("edges") or analysis.get("relationships") or [])

    st.markdown('<div id="kg-split-right-anchor"></div>', unsafe_allow_html=True)

    with st.container(border=True, key="insights_panel_card"):
        doc_icon = (
            f'<svg width="17" height="17" viewBox="0 0 24 24" fill="none">'
            f'<path d="M6 3H14L19 8V21H6V3Z" stroke="{t["accent"]}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<path d="M14 3V8H19M9 12H16M9 16H14" stroke="{t["accent"]}" stroke-width="1.5" stroke-linecap="round"/>'
            f"</svg>"
        )
        status_badge = render_status_badge(str(analysis.get("status") or "completed"), theme_name)
        st.markdown(
            f'<div class="kg-panel-hdr-row">'
            f'<div class="kg-panel-hdr-title">{doc_icon}<span>Document Insights</span></div>'
            f"{status_badge}"
            f"</div>",
            unsafe_allow_html=True,
        )

        # 1. Key Entities (clickable pills that isolate in Knowledge Graph)
        st.markdown(
            f'<div class="kg-insight-hdr" style="margin-top:0.15rem;"><span>Key Entities</span>'
            f'<span class="kg-mono" style="font-size:0.7rem; color:{t["text_secondary"]};">({len(nodes)})</span></div>',
            unsafe_allow_html=True,
        )
        if nodes:
            sorted_nodes = sorted(
                nodes,
                key=lambda n: (int(n.get("degree", 0)), int(n.get("occurrences", 1))),
                reverse=True,
            )[:8]
            pending_focus_key = f"_pending_focus_{aid}"
            col_count = 2 if len(sorted_nodes) > 1 else 1
            ent_cols = st.columns(col_count, gap="small")
            for idx, node in enumerate(sorted_nodes):
                lbl = str(node.get("label") or "")
                cat = str(node.get("category") or "Concept")
                occ = int(node.get("occurrences", 1))
                with ent_cols[idx % col_count]:
                    if st.button(
                        lbl,
                        key=f"insights_focus_ent_{aid}_{node.get('id', idx)}_{idx}",
                        help=f"{cat} · {occ} mention(s) — click to focus in Knowledge Graph",
                        use_container_width=True,
                    ):
                        if node.get("id"):
                            st.session_state[pending_focus_key] = node["id"]
                            st.session_state[f"graph_selected_node_{aid}"] = node["id"]
                            st.rerun()
        else:
            st.markdown('<div class="kg-muted">No domain entities extracted.</div>', unsafe_allow_html=True)

        # 2. Key Relations (concise bullet triples)
        st.markdown(
            f'<div class="kg-insight-hdr"><span>Key Relations</span>'
            f'<span class="kg-mono" style="font-size:0.7rem; color:{t["text_secondary"]};">({len(edges)})</span></div>',
            unsafe_allow_html=True,
        )
        with st.container(height=180, border=False):
            if edges:
                rel_items = []
                for edge in edges[:20]:
                    subj = escape_text(edge.get("source_label") or edge.get("subject") or edge.get("source"))
                    obj = escape_text(edge.get("target_label") or edge.get("object") or edge.get("target"))
                    rel = escape_text(str(edge.get("relation") or edge.get("relationship") or "").replace("_", " ").lower())
                    ref = escape_text(edge.get("source_ref") or f"Page {edge.get('page_number', '?')}")
                    rel_items.append(
                        f'<div class="kg-relation-bullet">'
                        f"&bull; <strong>{subj}</strong> "
                        f'<span style="color:{t["accent"]}; font-weight:500;">{rel}</span> '
                        f"<strong>{obj}</strong> "
                        f'<span class="kg-mono" style="font-size:0.68rem; color:{t["text_secondary"]};">({ref})</span>'
                        f"</div>"
                    )
                st.markdown("".join(rel_items), unsafe_allow_html=True)
            else:
                st.markdown(
                    '<div class="kg-muted" style="font-size:0.83rem;">No entity relationships were extracted.</div>',
                    unsafe_allow_html=True,
                )

        # 3. Summary
        src_label = "PDF Research Paper" if analysis.get("source_type") == "pdf" else "Pasted Text"
        author_txt = analysis.get("author") or "Not explicitly specified"
        summary_text = _derive_document_summary(analysis)
        st.markdown(
            f"""
            <div class="kg-insight-hdr"><span>Summary</span></div>
            <div style="font-size:0.84rem; color:{t['text_primary']}; line-height:1.55; margin-bottom:0.45rem; overflow-wrap:anywhere;">
                {escape_text(summary_text)}
            </div>
            <div class="kg-mono" style="font-size:0.71rem; color:{t['text_secondary']}; margin-bottom:0.75rem;">
                {src_label} &middot; Authors: {escape_text(author_txt)}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 4. Detailed Report Navigation CTA
        if on_navigate:
            if st.button(
                "View Detailed Report ->",
                key=f"insights_open_report_btn_{aid}",
                type="primary",
                use_container_width=True,
            ):
                on_navigate("Generate Report")


def render(
    api_client: APIClient,
    analysis: Optional[Dict[str, Any]],
    on_navigate: Optional[Callable[[str], None]] = None,
) -> None:
    theme_name = init_theme()
    split_pct = init_split_ratio()

    if not analysis:
        render_global_header(
            "Explore Knowledge",
            "Inspect the interactive knowledge graph alongside structured document insights.",
            eyebrow="02 // GRAPH EXPLORER & INSIGHTS",
            active_doc=None,
            theme_name=theme_name,
            on_toggle_theme=toggle_theme,
        )
        render_empty_state(
            "No Active Document Selected",
            "Upload a PDF or paste research text in Analyze Document to inspect its knowledge graph and structured insights.",
            kicker="Explore Knowledge",
        )
        if on_navigate and st.button("Go to Analyze Document", key="explore_empty_nav_btn", type="primary"):
            on_navigate("Analyze Document")
        return

    aid = analysis["analysis_id"]
    img_res = api_client.get(f"/api/analyses/{aid}/graph/image", timeout=30)
    action_clicked = render_global_header(
        "Explore Knowledge",
        "Inspect the interactive knowledge graph alongside structured document insights.",
        eyebrow="02 // GRAPH EXPLORER & INSIGHTS",
        active_doc=analysis,
        theme_name=theme_name,
        on_toggle_theme=toggle_theme,
        action_label="Generate Report ->",
        action_key="explore_header_report_btn",
    )
    if action_clicked and on_navigate:
        on_navigate("Generate Report")

    # Equal-height KPI Strip
    render_metric_cards(
        [
            ("Entities", analysis.get("entity_count", 0), "Normalized graph nodes"),
            ("Relationships", analysis.get("relationship_count", 0), "Directed semantic triples"),
            ("Categories", analysis.get("category_count", 0), "Scientific domains"),
            ("Passages", analysis.get("passage_count", 0), "Indexed evidence chunks"),
        ]
    )

    # Secondary toolbar: optional Graph PNG export + reset split width
    tb_left, tb_mid, tb_right = st.columns([2.6, 1.05, 1.05], vertical_alignment="center", gap="small")
    with tb_left:
        t = get_tokens(theme_name)
        st.markdown(
            f'<div class="kg-mono" style="font-size:0.73rem; color:{t["text_secondary"]};">'
            f"RESIZABLE WORKSPACE // DRAG VERTICAL DIVIDER TO ADJUST PANEL WIDTHS</div>",
            unsafe_allow_html=True,
        )
    with tb_mid:
        if img_res.ok and isinstance(img_res.data, (bytes, bytearray)):
            st.download_button(
                "Download Graph PNG",
                data=bytes(img_res.data),
                file_name=f"KnowledgeGraphAI_{aid}_graph.png",
                mime="image/png",
                key=f"explore_dl_graph_{aid}",
                use_container_width=True,
            )
    with tb_right:
        if st.button("Reset Split (62/38)", key=f"reset_split_btn_{aid}", use_container_width=True):
            st.session_state["explore_split_pct"] = 62.0
            st.query_params["split"] = "62.0"
            components.html(
                "<script>try{window.parent.localStorage.setItem('kgai_explore_split_pct','62.0');}catch(_){}</script>",
                height=0,
            )
            st.rerun()

    # Side-by-side resizable columns
    graph_col, insights_col = st.columns([split_pct, 100.0 - split_pct], gap="small")
    with graph_col:
        _render_graph_workspace(analysis, theme_name)
    with insights_col:
        _render_document_insights(analysis, theme_name, on_navigate)

    _inject_resizable_split_controller(split_pct)
