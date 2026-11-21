"""Centralized Industrial / Architectural design tokens, palettes, and CSS injection."""

from __future__ import annotations

import html
from typing import Dict

import streamlit as st

THEME_ORDER = ("obsidian", "limestone")

THEMES: Dict[str, Dict[str, str]] = {
    "obsidian": {
        "name": "obsidian",
        "label": "Obsidian",
        "mode_caption": "Dark",
        "bg_main": "#171918",
        "surface": "#202321",
        "surface_elevated": "#2B302D",
        "accent": "#B69A60",
        "accent_hover": "#C5AA72",
        "accent_text": "#171918",
        "accent_muted": "rgba(182, 154, 96, 0.14)",
        "text_primary": "#E8E4DA",
        "text_secondary": "#A7ADA6",
        "border": "#3B403C",
        "hover": "#303632",
        "success": "#6E8B74",
        "warning": "#C59B57",
        "error": "#B56B52",
        "info": "#6B7D8C",
        "code_bg": "#1B1E1C",
        "graph_bg": "#171918",
        "graph_grid": "rgba(167, 173, 166, 0.08)",
        "graph_edge": "#59615B",
        "graph_edge_dim": "rgba(89, 97, 91, 0.22)",
        "graph_edge_label": "#A7ADA6",
        "shadow": "0 1px 2px rgba(0, 0, 0, 0.38)",
        "color_scheme": "dark",
    },
    "limestone": {
        "name": "limestone",
        "label": "Limestone",
        "mode_caption": "Light",
        "bg_main": "#F2F0E9",
        "surface": "#FFFFFF",
        "surface_elevated": "#E7E4DA",
        "accent": "#927744",
        "accent_hover": "#7D6437",
        "accent_text": "#FFFFFF",
        "accent_muted": "rgba(146, 119, 68, 0.11)",
        "text_primary": "#252925",
        "text_secondary": "#686D65",
        "border": "#D8D5CA",
        "hover": "#EAE7DE",
        "success": "#4E6E58",
        "warning": "#A57A35",
        "error": "#A3523B",
        "info": "#536778",
        "code_bg": "#ECE9E0",
        "graph_bg": "#F2F0E9",
        "graph_grid": "rgba(37, 41, 37, 0.06)",
        "graph_edge": "#9EA39A",
        "graph_edge_dim": "rgba(158, 163, 154, 0.24)",
        "graph_edge_label": "#535850",
        "shadow": "0 1px 2px rgba(37, 41, 37, 0.08)",
        "color_scheme": "light",
    },
}

ENTITY_PALETTES: Dict[str, Dict[str, str]] = {
    "obsidian": {
        "Concept": "#B69A60",       # Antique brass
        "Model": "#6E8B74",         # Muted sage
        "Algorithm": "#6B7D8C",     # Dusty blue-grey
        "Organization": "#B56B52",  # Terracotta
        "Dataset": "#858C5E",       # Muted olive
        "Metric": "#8E8A80",        # Architectural stone
        "Task": "#547F7D",          # Desaturated teal
        "Technology": "#A86F4C",    # Warm copper
        "Framework": "#7E7B69",     # Slate bronze
        "Optimizer": "#9A7D56",     # Patina ochre
        "Method": "#6B7D8C",        # Dusty blue-grey
        "Author": "#8A8D87",        # Charcoal pewter
        "Paper": "#B69A60",         # Antique brass
        "Person": "#C49A6C",        # Warm sand brass
        "Group": "#7E9A84",         # Sage fern
        "Project": "#5F8D8B",       # Patina teal
        "Location": "#9D8468",      # Earth ochre
        "Product": "#8D9B6E",       # Harvest olive
    },
    "limestone": {
        "Concept": "#927744",       # Antique brass
        "Model": "#4E6E58",         # Muted sage
        "Algorithm": "#526474",     # Dusty blue-grey
        "Organization": "#A1583F",  # Terracotta
        "Dataset": "#6D7546",       # Muted olive
        "Metric": "#726E65",        # Stone
        "Task": "#3E6866",          # Desaturated teal
        "Technology": "#8F5938",    # Warm copper
        "Framework": "#666352",     # Slate bronze
        "Optimizer": "#7F6440",     # Patina ochre
        "Method": "#526474",        # Dusty blue-grey
        "Author": "#686D65",        # Slate grey
        "Paper": "#927744",         # Antique brass
        "Person": "#9C6E44",        # Warm bronze
        "Group": "#4E6E58",         # Forest sage
        "Project": "#3E6866",       # Deep teal
        "Location": "#7C6447",      # Umber
        "Product": "#647242",       # Moss olive
    },
}


def init_theme() -> str:
    """Resolve and synchronize the active theme across session_state and query_params."""
    qp_theme = str(st.query_params.get("theme", "")).strip().lower()
    ss_theme = str(st.session_state.get("theme", "")).strip().lower()

    if ss_theme in THEMES:
        active = ss_theme
    elif qp_theme in THEMES:
        active = qp_theme
    else:
        active = "obsidian"

    st.session_state["theme"] = active
    if st.query_params.get("theme") != active:
        st.query_params["theme"] = active
    return active


def set_theme(theme_name: str) -> str:
    """Persist a validated theme choice."""
    resolved = theme_name if theme_name in THEMES else "obsidian"
    st.session_state["theme"] = resolved
    st.query_params["theme"] = resolved
    return resolved


def toggle_theme() -> str:
    """Switch between Obsidian (dark) and Limestone (light)."""
    current = init_theme()
    nxt = "limestone" if current == "obsidian" else "obsidian"
    return set_theme(nxt)


def init_sidebar_state() -> bool:
    """Resolve and synchronize persistent sidebar collapse preference."""
    if "sidebar_collapsed" in st.session_state:
        collapsed = bool(st.session_state["sidebar_collapsed"])
    else:
        qp_val = str(st.query_params.get("sidebar", "")).strip().lower()
        collapsed = qp_val == "collapsed"
    st.session_state["sidebar_collapsed"] = collapsed
    desired_qp = "collapsed" if collapsed else "expanded"
    if st.query_params.get("sidebar") != desired_qp:
        st.query_params["sidebar"] = desired_qp
    return collapsed


def set_sidebar_collapsed(collapsed: bool) -> bool:
    """Persist sidebar collapsed/expanded preference across reruns and reloads."""
    resolved = bool(collapsed)
    st.session_state["sidebar_collapsed"] = resolved
    st.query_params["sidebar"] = "collapsed" if resolved else "expanded"
    return resolved


MIN_SPLIT_PCT = 35.0
MAX_SPLIT_PCT = 74.0
DEFAULT_SPLIT_PCT = 62.0


def init_split_ratio() -> float:
    """Resolve and clamp Explore Knowledge Knowledge-Graph/Insights width percentage."""
    raw = st.session_state.get("explore_split_pct")
    if raw is None:
        raw = st.query_params.get("split")
    try:
        pct = float(raw) if raw is not None else DEFAULT_SPLIT_PCT
    except (TypeError, ValueError):
        pct = DEFAULT_SPLIT_PCT
    pct = max(MIN_SPLIT_PCT, min(MAX_SPLIT_PCT, pct))
    st.session_state["explore_split_pct"] = pct
    return pct


def get_tokens(theme_name: str | None = None) -> Dict[str, str]:
    """Return design tokens for the requested or active theme."""
    name = theme_name if theme_name in THEMES else init_theme()
    return THEMES[name]


def get_entity_color(category: str, theme_name: str | None = None) -> str:
    """Return the curated scientific color for an entity category."""
    resolved = theme_name if theme_name in ENTITY_PALETTES else init_theme()
    palette = ENTITY_PALETTES[resolved]
    return palette.get(str(category or "").strip(), palette["Concept"])


def inject_theme_css(theme_name: str | None = None) -> Dict[str, str]:
    """Inject typography, custom properties, and full dual-theme Industrial CSS."""
    t = get_tokens(theme_name)
    css = f"""
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600&family=Manrope:wght@500;600;700&display=swap" rel="stylesheet" />
    <style>
        :root {{
            --primary-color: {t["accent"]};
            --background-color: {t["bg_main"]};
            --secondary-background-color: {t["surface"]};
            --text-color: {t["text_primary"]};
            --kg-bg: {t["bg_main"]};
            --kg-surface: {t["surface"]};
            --kg-elevated: {t["surface_elevated"]};
            --kg-accent: {t["accent"]};
            --kg-accent-hover: {t["accent_hover"]};
            --kg-accent-text: {t["accent_text"]};
            --kg-accent-muted: {t["accent_muted"]};
            --kg-text: {t["text_primary"]};
            --kg-text-muted: {t["text_secondary"]};
            --kg-border: {t["border"]};
            --kg-hover: {t["hover"]};
            --kg-success: {t["success"]};
            --kg-warning: {t["warning"]};
            --kg-error: {t["error"]};
            --kg-info: {t["info"]};
            --kg-code-bg: {t["code_bg"]};
            --kg-shadow: {t["shadow"]};
            --kg-sidebar-w: clamp(285px, 23.5vw, 355px);
            color-scheme: {t["color_scheme"]};
        }}

        html, body, .stApp, [data-testid="stAppViewContainer"] {{
            background-color: var(--kg-bg) !important;
            color: var(--kg-text) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        }}

        [data-testid="stHeader"] {{
            background-color: var(--kg-bg) !important;
            border-bottom: 1px solid var(--kg-border) !important;
        }}
        [data-testid="stAppViewContainer"]:has(#kg-left-sidebar-anchor) [data-testid="stHeader"] {{
            left: var(--kg-sidebar-w) !important;
            width: calc(100% - var(--kg-sidebar-w)) !important;
        }}

        /* Hide Streamlit built-in drawer so unified collapsible 25%/75% sidebar has full state control */
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapsedControl"] {{
            display: none !important;
        }}

        [data-testid="stToolbar"] button {{
            color: var(--kg-text-muted) !important;
        }}

        /* Full-width responsive workspace block */
        .block-container {{
            max-width: 100% !important;
            padding-top: 2.85rem !important;
            padding-bottom: 1.75rem !important;
            padding-left: 1.35rem !important;
            padding-right: 1.35rem !important;
            transition: padding 200ms ease, max-width 200ms ease;
        }}

        /* Typography hierarchy */
        h1, h2, h3, h4, .kg-heading {{
            font-family: 'Manrope', 'Inter', sans-serif !important;
            color: var(--kg-text) !important;
            letter-spacing: -0.02em;
        }}
        code, pre, .kg-mono, [data-testid="stMetricValue"] {{
            font-family: 'IBM Plex Mono', 'Consolas', monospace !important;
        }}
        p, li, span, label, div {{
            color: inherit;
        }}

        /* Left static full-height architectural sidebar column */
        [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) {{
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            bottom: 0 !important;
            height: 100vh !important;
            width: var(--kg-sidebar-w) !important;
            min-width: var(--kg-sidebar-w) !important;
            max-width: var(--kg-sidebar-w) !important;
            background-color: var(--kg-surface) !important;
            border: none !important;
            border-right: 1px solid var(--kg-border) !important;
            border-radius: 0 !important;
            padding: 0.55rem 0.85rem 0.45rem 0.85rem !important;
            margin: 0 !important;
            box-sizing: border-box !important;
            box-shadow: var(--kg-shadow);
            z-index: 999992 !important;
            display: flex !important;
            flex-direction: column !important;
            overflow-y: auto !important;
            overflow-x: hidden !important;
            transition: width 220ms ease, flex 220ms ease, opacity 180ms ease;
        }}
        [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stMarkdownContainer"] {{
            margin-bottom: 0 !important;
        }}
        [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stElementContainer"]:has(#kg-left-sidebar-anchor) {{
            height: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
        }}
        [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stElementContainer"]:has(iframe) {{
            position: absolute !important;
            width: 0 !important;
            height: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            pointer-events: none !important;
        }}
        html.kg-sidebar-resizing [data-testid="stColumn"]:has(#kg-left-sidebar-anchor),
        html.kg-sidebar-resizing [data-testid="stColumn"]:has(#kg-main-workspace-anchor),
        html.kg-sidebar-resizing [data-testid="stHeader"] {{
            transition: none !important;
        }}
        .kg-sidebar-resizer {{
            position: fixed;
            top: 0;
            bottom: 0;
            left: calc(var(--kg-sidebar-w) - 5px);
            width: 10px;
            cursor: col-resize;
            z-index: 999993;
            display: flex;
            align-items: center;
            justify-content: center;
            user-select: none;
            touch-action: none;
        }}
        .kg-sidebar-resizer::before {{
            content: "";
            width: 2px;
            height: 100%;
            background-color: transparent;
            transition: background-color 140ms ease, width 140ms ease;
        }}
        .kg-sidebar-resizer::after {{
            content: "⋮";
            position: fixed;
            top: 50%;
            left: calc(var(--kg-sidebar-w) - 7px);
            transform: translateY(-50%);
            font-family: 'IBM Plex Mono', monospace;
            font-size: 11px;
            font-weight: 700;
            line-height: 1;
            padding: 8px 2px;
            border-radius: 4px;
            background-color: var(--kg-elevated);
            border: 1px solid var(--kg-border);
            color: var(--kg-text-muted);
            box-shadow: var(--kg-shadow);
            opacity: 0.8;
            transition: opacity 140ms ease, border-color 140ms ease, color 140ms ease;
        }}
        .kg-sidebar-resizer:hover::before,
        .kg-sidebar-resizer.kg-dragging::before {{
            background-color: var(--kg-accent);
            width: 3px;
        }}
        .kg-sidebar-resizer:hover::after,
        .kg-sidebar-resizer.kg-dragging::after {{
            opacity: 1;
            border-color: var(--kg-accent);
            color: var(--kg-accent);
            background-color: var(--kg-surface);
        }}
        [data-testid="stAppViewContainer"]:not(:has(#kg-left-sidebar-anchor)) .kg-sidebar-resizer {{
            display: none !important;
        }}
        [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) > div {{
            flex: 1 1 auto !important;
            min-height: 0 !important;
            height: auto !important;
            max-height: 100% !important;
            display: flex !important;
            flex-direction: column !important;
            box-sizing: border-box !important;
        }}
        [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) > div > [data-testid="stVerticalBlock"],
        [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] #kg-left-sidebar-anchor) {{
            flex: 1 1 auto !important;
            min-height: 0 !important;
            height: auto !important;
            display: flex !important;
            flex-direction: column !important;
            gap: 0.14rem !important;
        }}
        [data-testid="stHorizontalBlock"]:has([data-testid="stColumn"] #kg-left-sidebar-anchor) > [data-testid="stColumn"]:has(#kg-main-workspace-anchor) {{
            margin-left: calc(var(--kg-sidebar-w) - 0.15rem) !important;
            width: calc(100% - (var(--kg-sidebar-w) - 0.15rem)) !important;
            flex: 1 1 calc(100% - (var(--kg-sidebar-w) - 0.15rem)) !important;
            min-width: 0 !important;
            transition: width 220ms ease, flex 220ms ease, margin-left 220ms ease;
        }}
        [data-testid="stColumn"]:has(#kg-main-workspace-anchor) {{
            min-width: 0;
            transition: width 220ms ease, flex 220ms ease;
        }}

        /* Brand card inside sidebar */
        .kg-brand-box {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.6rem;
            padding: 0 0 0.38rem 0;
            border-bottom: 1px solid var(--kg-border);
            margin-bottom: 0.12rem;
        }}
        .kg-brand-left {{
            display: flex;
            align-items: center;
            gap: 0.65rem;
            min-width: 0;
        }}
        .kg-brand-title {{
            font-family: 'Manrope', sans-serif;
            font-weight: 700;
            font-size: 1rem;
            color: var(--kg-text);
            letter-spacing: -0.015em;
            line-height: 1.15;
        }}
        .kg-brand-tagline {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.64rem;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            color: var(--kg-accent);
            margin-top: 0.15rem;
        }}
        .kg-sidebar-section-label {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--kg-text-muted);
            margin: 0.14rem 0 0.08rem 0;
        }}
        .kg-workspace-heading {{
            font-family: 'Manrope', 'Inter', sans-serif !important;
            font-size: 0.96rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.12em !important;
            color: var(--kg-text) !important;
            margin: 0.08rem 0 0.08rem 0 !important;
            padding-bottom: 0.12rem;
            border-bottom: 1px solid var(--kg-border);
        }}

        /* Sidebar Radio Navigation (Enlarged Workspace Items) */
        [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stRadio"] > div {{
            gap: 0.14rem !important;
        }}
        [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stRadio"] label {{
            background-color: transparent !important;
            border: 1px solid transparent !important;
            border-radius: 6px !important;
            padding: 0.28rem 0.68rem !important;
            transition: background-color 140ms ease, border-color 140ms ease;
            margin: 0 !important;
            width: 100%;
        }}
        [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stRadio"] label:hover {{
            background-color: var(--kg-hover) !important;
            border-color: var(--kg-border) !important;
        }}
        [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stRadio"] label p {{
            color: var(--kg-text) !important;
            font-size: 1.02rem !important;
            font-weight: 600 !important;
            line-height: 1.28 !important;
        }}
        [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stRadio"] label[data-checked="true"],
        [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {{
            background-color: var(--kg-accent-muted) !important;
            border-color: var(--kg-accent) !important;
        }}
        [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p {{
            color: var(--kg-accent) !important;
            font-weight: 700 !important;
        }}
        [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stButton"] button {{
            min-height: 34px !important;
            padding: 0.28rem 0.65rem !important;
        }}

        /* Upper Workspace + Documents scroll region (yields smoothly when Ask Me slides up) */
        [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stLayoutWrapper"]:has(> .st-key-sidebar_top_nav),
        [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stElementContainer"]:has(> .st-key-sidebar_top_nav),
        .stApp .st-key-sidebar_top_nav {{
            flex: 0 1 auto !important;
            min-height: 60px !important;
            overflow-y: auto !important;
            overflow-x: hidden !important;
            padding: 0 0.1rem 0.25rem 0 !important;
            margin: 0 !important;
            border: none !important;
            gap: 0.14rem !important;
        }}
        .stApp .st-key-sidebar_top_nav [data-testid="stVerticalBlock"] {{
            gap: 0.14rem !important;
        }}

        /* Boxed Ask Me Card inside Sidebar — defaults to ~48% and slides vertically */
        [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stLayoutWrapper"]:has(> .st-key-askme_card),
        [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stElementContainer"]:has(> .st-key-askme_card) {{
            flex: 0 0 var(--kg-askme-h, 48vh) !important;
            height: var(--kg-askme-h, 48vh) !important;
            max-height: calc(100vh - 140px) !important;
            min-height: 200px !important;
            display: flex !important;
            flex-direction: column !important;
            margin-top: auto !important;
            padding-top: 6px !important;
        }}
        .stApp .st-key-askme_card {{
            position: relative !important;
            background-color: var(--kg-bg) !important;
            border: 1px solid var(--kg-border) !important;
            border-top: 2px solid var(--kg-accent) !important;
            border-radius: 8px !important;
            padding: 0.56rem 0.7rem 0.48rem 0.7rem !important;
            margin-top: 0 !important;
            height: 100% !important;
            max-height: calc(100vh - 140px) !important;
            min-height: 200px !important;
            flex: 1 1 auto !important;
            display: flex !important;
            flex-direction: column !important;
        }}
        html.kg-askme-resizing .st-key-askme_card,
        html.kg-askme-resizing [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stLayoutWrapper"]:has(> .st-key-askme_card),
        html.kg-askme-resizing [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stElementContainer"]:has(> .st-key-askme_card) {{
            transition: none !important;
        }}
        .kg-askme-resizer {{
            position: absolute;
            top: -7px;
            left: 10px;
            right: 10px;
            height: 12px;
            cursor: row-resize;
            z-index: 30;
            display: flex;
            align-items: center;
            justify-content: center;
            user-select: none;
            touch-action: none;
        }}
        .kg-askme-resizer::before {{
            content: "";
            height: 2px;
            width: 100%;
            background-color: transparent;
            border-radius: 2px;
            transition: background-color 140ms ease, height 140ms ease;
        }}
        .kg-askme-resizer::after {{
            content: "⋯";
            position: absolute;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 11px;
            font-weight: 700;
            line-height: 1;
            padding: 1px 10px;
            border-radius: 4px;
            background-color: var(--kg-elevated);
            border: 1px solid var(--kg-border);
            color: var(--kg-text-muted);
            box-shadow: var(--kg-shadow);
            opacity: 0.85;
            transition: opacity 140ms ease, border-color 140ms ease, color 140ms ease, background-color 140ms ease;
        }}
        .kg-askme-resizer:hover::before,
        .kg-askme-resizer.kg-dragging::before {{
            background-color: var(--kg-accent);
            height: 3px;
        }}
        .kg-askme-resizer:hover::after,
        .kg-askme-resizer.kg-dragging::after {{
            opacity: 1;
            border-color: var(--kg-accent);
            color: var(--kg-accent);
            background-color: var(--kg-surface);
        }}
        .stApp .st-key-askme_card > [data-testid="stVerticalBlock"],
        .stApp .st-key-askme_card > div > [data-testid="stVerticalBlock"] {{
            display: flex !important;
            flex-direction: column !important;
            height: 100% !important;
            min-height: 100% !important;
            gap: 0.25rem !important;
        }}
        .stApp .st-key-askme_card [data-testid="stLayoutWrapper"]:has(.st-key-askme_messages),
        .stApp .st-key-askme_card [data-testid="stVerticalBlock"] > div:has(> .st-key-askme_messages),
        .stApp .st-key-askme_messages {{
            flex: 1 1 auto !important;
            min-height: 0 !important;
            max-height: none !important;
            overflow-y: auto !important;
            overflow-x: hidden !important;
            padding-right: 0.15rem !important;
        }}
        .stApp .st-key-askme_card [data-testid="stElementContainer"]:has(.kg-askme-input-sep) {{
            margin-top: auto !important;
        }}
        .kg-askme-empty {{
            background-color: var(--kg-surface);
            border: 1px dashed var(--kg-border);
            border-radius: 6px;
            padding: 0.55rem 0.65rem;
            font-size: 0.77rem;
            color: var(--kg-text-muted);
            line-height: 1.42;
            margin-bottom: 0.35rem;
        }}
        .kg-askme-input-sep {{
            border-top: 1px solid var(--kg-border);
            margin: 0.4rem 0 0.45rem 0;
        }}
        .stApp .st-key-askme_card [data-testid="stForm"] [data-testid="stHorizontalBlock"] {{
            gap: 0.35rem !important;
        }}
        .stApp .st-key-askme_card [data-testid="stFormSubmitButton"] button {{
            padding: 0.25rem 0.42rem !important;
            white-space: nowrap !important;
            min-height: 36px !important;
            font-size: 0.8rem !important;
            line-height: 1.1 !important;
        }}
        .kg-sidebar-chat-hdr {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.4rem;
            padding-bottom: 0.42rem;
            border-bottom: 1px solid var(--kg-border);
            margin-bottom: 0.35rem;
        }}
        .kg-sidebar-chat-title {{
            display: inline-flex;
            align-items: center;
            gap: 0.42rem;
            font-family: 'Manrope', sans-serif;
            font-weight: 700;
            font-size: 0.94rem;
            color: var(--kg-text);
        }}
        [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stElementContainer"]:has(.kg-sidebar-status-footer) {{
            margin-top: 0.14rem !important;
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }}
        [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stElementContainer"]:has(.kg-sidebar-status-footer) [data-testid="stMarkdownContainer"] {{
            margin-bottom: 0 !important;
        }}
        .kg-sidebar-status-footer {{
            margin-top: 0.1rem;
            margin-bottom: 0;
            padding-top: 0.42rem;
            border-top: 1px solid var(--kg-border);
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
        }}
        .kg-status-line {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.7rem;
            color: var(--kg-text-muted);
        }}

        /* Global Header Bar */
        .kg-global-header {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 0.75rem;
            padding: 0.85rem 1.1rem;
            background-color: var(--kg-surface);
            border: 1px solid var(--kg-border);
            border-radius: 8px;
            margin-bottom: 1.1rem;
            box-shadow: var(--kg-shadow);
        }}
        .kg-header-left {{
            display: flex;
            flex-direction: column;
            gap: 0.22rem;
            min-width: 0;
        }}
        .kg-header-eyebrow {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.68rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--kg-accent);
        }}
        .kg-header-title {{
            font-family: 'Manrope', sans-serif;
            font-size: 1.48rem;
            font-weight: 700;
            color: var(--kg-text);
            margin: 0;
            line-height: 1.2;
        }}
        .kg-header-subtitle {{
            font-size: 0.9rem;
            color: var(--kg-text-muted);
            margin: 0;
        }}
        .kg-active-doc-pill {{
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.3rem 0.65rem;
            border-radius: 5px;
            background-color: var(--kg-elevated);
            border: 1px solid var(--kg-border);
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.76rem;
            color: var(--kg-text);
            max-width: 100%;
        }}
        .kg-status-dot {{
            width: 7px;
            height: 7px;
            border-radius: 999px;
            display: inline-block;
            flex-shrink: 0;
        }}

        /* Cards & Panels */
        .kg-card {{
            background-color: var(--kg-surface);
            border: 1px solid var(--kg-border);
            border-radius: 8px;
            padding: 1rem 1.15rem;
            margin-bottom: 0.85rem;
            box-shadow: var(--kg-shadow);
        }}
        .kg-card-elevated {{
            background-color: var(--kg-elevated);
            border: 1px solid var(--kg-border);
            border-radius: 8px;
            padding: 0.9rem 1.05rem;
            margin-bottom: 0.75rem;
        }}
        .kg-section-kicker {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--kg-accent);
            margin-bottom: 0.25rem;
        }}
        .kg-panel-title {{
            font-family: 'Manrope', sans-serif;
            font-size: 1.06rem;
            font-weight: 600;
            color: var(--kg-text);
            margin: 0 0 0.35rem 0;
        }}
        .kg-muted {{
            color: var(--kg-text-muted);
            font-size: 0.88rem;
        }}

        /* Equal-height compact KPI metric cards (icon left + value & label right) */
        .kg-metric-card {{
            background-color: var(--kg-surface);
            border: 1px solid var(--kg-border);
            border-radius: 8px;
            padding: 0.72rem 0.95rem;
            box-shadow: var(--kg-shadow);
            height: 100%;
            min-height: 76px;
            display: flex;
            align-items: center;
            gap: 0.85rem;
        }}
        .kg-metric-icon {{
            width: 36px;
            height: 36px;
            border-radius: 7px;
            background-color: var(--kg-accent-muted);
            border: 1px solid var(--kg-border);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}
        .kg-metric-body {{
            display: flex;
            flex-direction: column;
            min-width: 0;
        }}
        .kg-metric-value {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--kg-text);
            line-height: 1.08;
        }}
        .kg-metric-label {{
            font-family: 'Inter', sans-serif;
            font-size: 0.78rem;
            font-weight: 500;
            color: var(--kg-text-muted);
            margin-top: 0.14rem;
        }}
        .kg-metric-sub {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.67rem;
            color: var(--kg-text-muted);
            opacity: 0.82;
        }}

        /* Badges */
        .kg-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.18rem 0.55rem;
            border-radius: 4px;
            border: 1px solid var(--kg-border);
            background-color: var(--kg-elevated);
            color: var(--kg-text);
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.72rem;
            font-weight: 500;
            line-height: 1.3;
        }}
        .kg-badge-dot {{
            width: 7px;
            height: 7px;
            border-radius: 999px;
            display: inline-block;
        }}

        /* Processing stage list */
        .kg-stage-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.48rem 0.72rem;
            border-bottom: 1px solid var(--kg-border);
            font-size: 0.86rem;
        }}
        .kg-stage-row:last-child {{
            border-bottom: none;
        }}
        .kg-stage-index {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.75rem;
            color: var(--kg-accent);
            margin-right: 0.65rem;
        }}

        /* Dropzone polish */
        [data-testid="stFileUploaderDropzone"] {{
            background-color: var(--kg-surface) !important;
            border: 1.5px dashed var(--kg-accent) !important;
            border-radius: 8px !important;
            padding: 1.35rem 1rem !important;
            color: var(--kg-text) !important;
        }}
        [data-testid="stFileUploaderDropzone"]:hover {{
            background-color: var(--kg-hover) !important;
        }}
        [data-testid="stFileUploaderDropzoneInstructions"] span,
        [data-testid="stFileUploaderDropzoneInstructions"] small,
        [data-testid="stFileUploaderDropzone"] svg {{
            color: var(--kg-text-muted) !important;
            fill: var(--kg-text-muted) !important;
        }}
        [data-testid="stFileUploaderDropzone"] button {{
            background-color: var(--kg-elevated) !important;
            border: 1px solid var(--kg-border) !important;
            color: var(--kg-text) !important;
        }}
        [data-testid="stFileUploaderDropzone"] button:hover {{
            background-color: var(--kg-hover) !important;
            border-color: var(--kg-accent) !important;
        }}

        /* Widget Labels & Form Captions */
        [data-testid="stWidgetLabel"],
        [data-testid="stWidgetLabel"] p,
        [data-testid="stWidgetLabel"] label {{
            color: var(--kg-text) !important;
            font-weight: 500 !important;
        }}

        /* Buttons (Streamlit 1.66 BaseButton + standard buttons) */
        .stButton > button,
        .stDownloadButton > button,
        button[data-testid^="stBaseButton-secondary"],
        button[data-testid="stBaseButton-header"] {{
            border-radius: 6px !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 500 !important;
            font-size: 0.87rem !important;
            border: 1px solid var(--kg-border) !important;
            background-color: var(--kg-elevated) !important;
            color: var(--kg-text) !important;
            transition: background-color 140ms ease, border-color 140ms ease, color 140ms ease;
        }}
        .stButton > button p,
        .stDownloadButton > button p,
        button[data-testid^="stBaseButton-secondary"] p {{
            color: var(--kg-text) !important;
        }}
        .stButton > button:hover,
        .stDownloadButton > button:hover,
        button[data-testid^="stBaseButton-secondary"]:hover {{
            background-color: var(--kg-hover) !important;
            border-color: var(--kg-accent) !important;
            color: var(--kg-text) !important;
        }}
        .stButton > button[kind="primary"],
        .stDownloadButton > button[kind="primary"],
        button[data-testid="stBaseButton-primary"],
        button[data-testid="stBaseButton-primaryFormSubmit"] {{
            background-color: var(--kg-accent) !important;
            border-color: var(--kg-accent) !important;
            color: var(--kg-accent-text) !important;
            font-weight: 600 !important;
        }}
        .stButton > button[kind="primary"] p,
        .stDownloadButton > button[kind="primary"] p,
        button[data-testid="stBaseButton-primary"] p,
        button[data-testid="stBaseButton-primaryFormSubmit"] p {{
            color: var(--kg-accent-text) !important;
        }}
        .stButton > button[kind="primary"]:hover,
        .stDownloadButton > button[kind="primary"]:hover,
        button[data-testid="stBaseButton-primary"]:hover,
        button[data-testid="stBaseButton-primaryFormSubmit"]:hover {{
            background-color: var(--kg-accent-hover) !important;
            border-color: var(--kg-accent-hover) !important;
            color: var(--kg-accent-text) !important;
        }}
        .stButton > button:disabled,
        button[data-testid^="stBaseButton-"]:disabled {{
            opacity: 0.55 !important;
            cursor: not-allowed !important;
        }}

        /* Inputs, Textareas, Selectboxes */
        [data-baseweb="input"],
        [data-baseweb="base-input"],
        [data-baseweb="textarea"],
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stNumberInput"] input {{
            background-color: var(--kg-surface) !important;
            color: var(--kg-text) !important;
            -webkit-text-fill-color: var(--kg-text) !important;
            caret-color: var(--kg-accent) !important;
            border-color: var(--kg-border) !important;
            border-radius: 6px !important;
        }}
        [data-baseweb="input"] input::placeholder,
        [data-baseweb="textarea"] textarea::placeholder {{
            color: var(--kg-text-muted) !important;
            -webkit-text-fill-color: var(--kg-text-muted) !important;
            opacity: 0.88 !important;
        }}
        [data-baseweb="input"]:focus-within,
        [data-baseweb="textarea"]:focus-within,
        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus {{
            border-color: var(--kg-accent) !important;
            box-shadow: 0 0 0 1px var(--kg-accent) !important;
        }}
        html body .stApp [data-testid="stSelectbox"] div[data-baseweb="select"],
        html body .stApp [data-testid="stMultiSelect"] div[data-baseweb="select"],
        html body .stApp div[data-baseweb="select"] > div {{
            background-color: var(--kg-surface) !important;
            border: 1px solid var(--kg-border) !important;
            color: var(--kg-text) !important;
            border-radius: 6px !important;
        }}
        html body .stApp div[data-baseweb="select"] > div > div {{
            background-color: var(--kg-surface) !important;
        }}
        html body .stApp div[data-baseweb="select"] span,
        html body .stApp div[data-baseweb="select"] input,
        html body .stApp div[data-baseweb="select"] svg {{
            color: var(--kg-text) !important;
            fill: var(--kg-text-muted) !important;
        }}
        [data-baseweb="popover"],
        [data-baseweb="menu"],
        [data-baseweb="menu"] ul,
        [data-testid="stSelectboxVirtualDropdown"],
        [data-testid="stSelectboxVirtualDropdown"] ul {{
            background-color: var(--kg-surface) !important;
            color: var(--kg-text) !important;
            border: 1px solid var(--kg-border) !important;
        }}
        [data-baseweb="menu"] li,
        [data-baseweb="menu"] li span,
        [data-testid="stSelectboxVirtualDropdown"] li {{
            background-color: var(--kg-surface) !important;
            color: var(--kg-text) !important;
        }}
        [data-baseweb="menu"] li:hover,
        [data-testid="stSelectboxVirtualDropdown"] li:hover {{
            background-color: var(--kg-hover) !important;
        }}
        html body .stApp div[data-baseweb="select"] span[data-baseweb="tag"],
        html body .stApp span[data-baseweb="tag"] {{
            background-color: var(--kg-elevated) !important;
            border: 1px solid var(--kg-accent) !important;
            color: var(--kg-text) !important;
        }}
        html body .stApp span[data-baseweb="tag"] span,
        html body .stApp span[data-baseweb="tag"] svg {{
            color: var(--kg-text) !important;
            fill: var(--kg-text-muted) !important;
        }}

        /* Override Streamlit default red accents on radios & sliders */
        html body .stApp label[data-baseweb="radio"] > div:first-child {{
            border-color: var(--kg-accent) !important;
            background-color: transparent !important;
        }}
        html body .stApp label[data-baseweb="radio"] > div:first-child > div {{
            background-color: var(--kg-accent) !important;
        }}
        html body .stApp label[data-baseweb="radio"] p,
        html body .stApp [data-testid="stRadio"] label * {{
            color: var(--kg-text) !important;
        }}
        html body .stApp div[data-testid="stSlider"] div[role="slider"] {{
            background-color: var(--kg-accent) !important;
            border-color: var(--kg-accent) !important;
        }}
        html body .stApp div[data-testid="stSlider"] [data-baseweb="slider"] > div > div > div {{
            background-color: var(--kg-accent) !important;
        }}
        html body .stApp div[data-testid="stSlider"] [data-baseweb="slider"] > div > div {{
            background-color: var(--kg-border) !important;
        }}
        html body .stApp div[data-testid="stSliderThumbValue"],
        html body .stApp div[data-testid="stSliderTickBarMin"],
        html body .stApp div[data-testid="stSliderTickBarMax"] {{
            color: var(--kg-accent) !important;
            font-family: 'IBM Plex Mono', monospace !important;
        }}

        /* Tabs */
        html body .stApp .stTabs [data-baseweb="tab-list"] {{
            border-bottom: 1px solid var(--kg-border) !important;
            gap: 0.4rem !important;
            background-color: transparent !important;
        }}
        html body .stApp .stTabs [data-baseweb="tab"],
        html body .stApp .stTabs button[role="tab"] {{
            background-color: transparent !important;
            color: var(--kg-text-muted) !important;
            border: 1px solid transparent !important;
            border-radius: 6px 6px 0 0 !important;
            padding: 0.45rem 0.9rem !important;
            font-weight: 500 !important;
        }}
        html body .stApp .stTabs [data-baseweb="tab"] *,
        html body .stApp .stTabs button[role="tab"] *,
        html body .stApp button[data-baseweb="tab"] p {{
            color: var(--kg-text-muted) !important;
        }}
        html body .stApp .stTabs [aria-selected="true"],
        html body .stApp .stTabs button[role="tab"][aria-selected="true"] {{
            color: var(--kg-accent) !important;
            border-bottom: 2px solid var(--kg-accent) !important;
            background-color: var(--kg-accent-muted) !important;
        }}
        html body .stApp .stTabs [aria-selected="true"] *,
        html body .stApp .stTabs button[role="tab"][aria-selected="true"] *,
        html body .stApp button[data-baseweb="tab"][aria-selected="true"] p {{
            color: var(--kg-accent) !important;
            font-weight: 600 !important;
        }}
        html body .stApp .stTabs [data-baseweb="tab-highlight"] {{
            background-color: var(--kg-accent) !important;
        }}

        /* Expander & Alerts & Tables */
        [data-testid="stExpander"] {{
            background-color: var(--kg-surface) !important;
            border: 1px solid var(--kg-border) !important;
            border-radius: 7px !important;
        }}
        [data-testid="stExpander"] summary {{
            color: var(--kg-text) !important;
        }}
        [data-testid="stAlert"] {{
            background-color: var(--kg-elevated) !important;
            border: 1px solid var(--kg-border) !important;
            color: var(--kg-text) !important;
            border-radius: 7px !important;
        }}
        [data-testid="stDataFrame"] {{
            border: 1px solid var(--kg-border) !important;
            border-radius: 7px !important;
        }}

        /* Assistant Message Bubbles */
        .kg-msg-user {{
            background-color: var(--kg-elevated);
            border: 1px solid var(--kg-border);
            border-left: 3px solid var(--kg-accent);
            border-radius: 7px;
            padding: 0.58rem 0.72rem;
            margin-bottom: 0.45rem;
            overflow-wrap: anywhere;
            word-break: break-word;
            font-size: 0.84rem;
            line-height: 1.48;
        }}
        .kg-msg-assistant {{
            background-color: var(--kg-surface);
            border: 1px solid var(--kg-border);
            border-radius: 7px;
            padding: 0.65rem 0.75rem;
            margin-bottom: 0.35rem;
            overflow-wrap: anywhere;
            word-break: break-word;
            font-size: 0.84rem;
            line-height: 1.5;
        }}
        .kg-msg-meta {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.35rem;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.65rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--kg-text-muted);
            margin-bottom: 0.28rem;
        }}
        .kg-citation-card {{
            background-color: var(--kg-code-bg);
            border: 1px solid var(--kg-border);
            border-radius: 6px;
            padding: 0.5rem 0.68rem;
            margin-bottom: 0.38rem;
            font-size: 0.8rem;
            overflow-wrap: anywhere;
            word-break: break-word;
        }}
        .kg-citation-ref {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.72rem;
            color: var(--kg-accent);
            font-weight: 600;
        }}

        /* Enclosed Split Panel Cards (Knowledge Graph & Document Insights) */
        .stApp .st-key-kg_panel_card,
        .stApp .st-key-insights_panel_card {{
            background-color: var(--kg-surface) !important;
            border: 1px solid var(--kg-border) !important;
            border-radius: 8px !important;
            padding: 0.82rem 0.92rem !important;
            box-shadow: var(--kg-shadow);
            height: 100%;
        }}
        .kg-panel-hdr-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.5rem;
            padding-bottom: 0.55rem;
            border-bottom: 1px solid var(--kg-border);
            margin-bottom: 0.65rem;
        }}
        .kg-panel-hdr-title {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            font-family: 'Manrope', sans-serif;
            font-size: 1.02rem;
            font-weight: 700;
            color: var(--kg-text);
        }}
        .kg-insight-hdr {{
            display: inline-flex;
            align-items: center;
            gap: 0.42rem;
            font-family: 'Manrope', sans-serif;
            font-size: 0.86rem;
            font-weight: 700;
            color: var(--kg-text);
            margin: 0.55rem 0 0.35rem 0;
        }}
        .kg-relation-bullet {{
            font-size: 0.83rem;
            color: var(--kg-text);
            line-height: 1.48;
            padding: 0.22rem 0;
            border-bottom: 1px solid var(--kg-border);
            overflow-wrap: anywhere;
        }}
        .kg-relation-bullet:last-child {{
            border-bottom: none;
        }}

        /* Resizable Split Container & Prominent Draggable Handle */
        [data-testid="stHorizontalBlock"]:has([data-testid="stColumn"]:not(:has(#kg-main-workspace-anchor)) #kg-split-left-anchor) {{
            align-items: stretch !important;
            gap: 0 !important;
            position: relative;
            flex-wrap: nowrap !important;
        }}
        [data-testid="stHorizontalBlock"].kg-split-stacked {{
            flex-direction: column !important;
            flex-wrap: wrap !important;
            gap: 0.9rem !important;
        }}
        [data-testid="stHorizontalBlock"].kg-split-stacked > [data-testid="stColumn"] {{
            width: 100% !important;
            flex: 1 1 100% !important;
            max-width: 100% !important;
            min-width: 0 !important;
        }}
        [data-testid="stHorizontalBlock"].kg-split-stacked > .kg-split-resizer {{
            display: none !important;
        }}
        [data-testid="stColumn"]:not(:has(#kg-main-workspace-anchor)):has(#kg-split-left-anchor) {{
            min-width: 420px;
            transition: flex 50ms linear;
        }}
        [data-testid="stColumn"]:not(:has(#kg-main-workspace-anchor)):has(#kg-split-right-anchor) {{
            min-width: 300px;
            transition: flex 50ms linear;
        }}
        .kg-split-resizer {{
            flex: 0 0 18px;
            width: 18px;
            cursor: col-resize;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            user-select: none;
            z-index: 20;
            margin: 0 2px;
        }}
        .kg-split-resizer::before {{
            content: "";
            width: 2px;
            height: 100%;
            min-height: 240px;
            background-color: var(--kg-border);
            border-radius: 2px;
            transition: background-color 140ms ease, width 140ms ease;
        }}
        .kg-split-resizer::after {{
            content: "↔";
            position: sticky;
            top: 46vh;
            font-size: 11px;
            font-family: 'IBM Plex Mono', monospace;
            font-weight: 600;
            line-height: 1;
            padding: 8px 3px;
            border-radius: 5px;
            background-color: var(--kg-elevated);
            border: 1px solid var(--kg-border);
            color: var(--kg-text-muted);
            box-shadow: var(--kg-shadow);
            transition: border-color 140ms ease, color 140ms ease, background-color 140ms ease;
        }}
        .kg-split-resizer:hover::before,
        .kg-split-resizer.kg-dragging::before {{
            background-color: var(--kg-accent);
            width: 3px;
        }}
        .kg-split-resizer:hover::after,
        .kg-split-resizer.kg-dragging::after {{
            border-color: var(--kg-accent);
            color: var(--kg-accent);
            background-color: var(--kg-surface);
        }}

        /* Academic Report Typography */
        .kg-report-paper {{
            background-color: var(--kg-surface);
            border: 1px solid var(--kg-border);
            border-radius: 8px;
            padding: 1.65rem 1.9rem;
            box-shadow: var(--kg-shadow);
            max-width: 980px;
            margin: 0 auto 1.25rem auto;
        }}
        .kg-report-banner {{
            border-bottom: 2px solid var(--kg-accent);
            padding-bottom: 1rem;
            margin-bottom: 1.25rem;
        }}
        .kg-report-section {{
            padding-top: 0.85rem;
            margin-top: 0.85rem;
            border-top: 1px solid var(--kg-border);
        }}
        .kg-report-section h3 {{
            font-family: 'Manrope', sans-serif !important;
            font-size: 1.06rem !important;
            font-weight: 700 !important;
            margin-bottom: 0.45rem !important;
        }}
        .kg-report-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
            margin-top: 0.5rem;
        }}
        .kg-report-table th {{
            text-align: left;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            padding: 0.5rem 0.65rem;
            background-color: var(--kg-elevated);
            border-bottom: 1px solid var(--kg-border);
            color: var(--kg-text-muted);
        }}
        .kg-report-table td {{
            padding: 0.48rem 0.65rem;
            border-bottom: 1px solid var(--kg-border);
            color: var(--kg-text);
            vertical-align: top;
        }}

        /* Streamlit native chat input bar */
        [data-testid="stChatInput"] textarea {{
            background-color: var(--kg-surface) !important;
            color: var(--kg-text) !important;
            border-color: var(--kg-border) !important;
        }}

        /* Shorter desktop viewports (e.g. 1366x768): keep top + 50% Ask Me + System Status unclipped */
        @media (max-height: 820px) and (min-width: 961px) {{
            [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) {{
                padding: 0.52rem 0.78rem 0.45rem 0.78rem !important;
            }}
            [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) > div > [data-testid="stVerticalBlock"],
            [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] #kg-left-sidebar-anchor) {{
                gap: 0.16rem !important;
            }}
            .kg-brand-box {{
                padding: 0.05rem 0 0.35rem 0;
                margin-bottom: 0.12rem;
            }}
            .kg-workspace-heading {{
                font-size: 0.88rem !important;
                margin: 0.12rem 0 0.1rem 0 !important;
            }}
            [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stRadio"] label {{
                padding: 0.32rem 0.65rem !important;
            }}
            [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stRadio"] label p {{
                font-size: 0.96rem !important;
            }}
            [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stLayoutWrapper"]:has(> .st-key-askme_card),
            [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stElementContainer"]:has(> .st-key-askme_card) {{
                flex: 0 0 var(--kg-askme-h, 46vh) !important;
                height: var(--kg-askme-h, 46vh) !important;
                max-height: calc(100vh - 140px) !important;
                min-height: 200px !important;
            }}
            .stApp .st-key-askme_card {{
                height: 100% !important;
                max-height: calc(100vh - 140px) !important;
                min-height: 200px !important;
            }}
        }}

        /* Responsive stacking on smaller viewports (< 960px) */
        @media (max-width: 960px) {{
            .block-container {{
                padding-left: 0.85rem !important;
                padding-right: 0.85rem !important;
            }}
            [data-testid="stAppViewContainer"]:has(#kg-left-sidebar-anchor) [data-testid="stHeader"] {{
                left: 0 !important;
                width: 100% !important;
            }}
            [data-testid="stHorizontalBlock"]:has([data-testid="stColumn"] #kg-left-sidebar-anchor),
            [data-testid="stHorizontalBlock"]:has([data-testid="stColumn"]:not(:has(#kg-main-workspace-anchor)) #kg-split-left-anchor) {{
                flex-direction: column !important;
                flex-wrap: wrap !important;
                gap: 0.85rem !important;
            }}
            [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) {{
                position: static !important;
                top: auto !important;
                left: auto !important;
                bottom: auto !important;
                height: auto !important;
                min-height: auto !important;
                border: 1px solid var(--kg-border) !important;
                border-radius: 8px !important;
                z-index: auto !important;
                overflow: visible !important;
            }}
            [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) > div,
            [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) > div > [data-testid="stVerticalBlock"],
            [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] #kg-left-sidebar-anchor) {{
                height: auto !important;
                min-height: auto !important;
            }}
            [data-testid="stHorizontalBlock"]:has([data-testid="stColumn"] #kg-left-sidebar-anchor) > [data-testid="stColumn"]:has(#kg-main-workspace-anchor) {{
                margin-left: 0 !important;
                width: 100% !important;
                flex: 1 1 100% !important;
            }}
            [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stLayoutWrapper"]:has(> .st-key-askme_card),
            [data-testid="stColumn"]:has(#kg-left-sidebar-anchor) [data-testid="stElementContainer"]:has(> .st-key-askme_card),
            .stApp .st-key-askme_card {{
                flex: 0 0 auto !important;
                height: auto !important;
                min-height: 250px !important;
            }}
            [data-testid="stColumn"]:has(#kg-left-sidebar-anchor),
            [data-testid="stColumn"]:has(#kg-main-workspace-anchor),
            [data-testid="stColumn"]:not(:has(#kg-main-workspace-anchor)):has(#kg-split-left-anchor),
            [data-testid="stColumn"]:not(:has(#kg-main-workspace-anchor)):has(#kg-split-right-anchor) {{
                width: 100% !important;
                flex: 1 1 100% !important;
                max-width: 100% !important;
                min-width: 0 !important;
            }}
            .kg-sidebar-resizer,
            .kg-askme-resizer,
            .kg-split-resizer {{
                display: none !important;
            }}
        }}

        /* Print optimization */
        @media print {{
            [data-testid="stColumn"]:has(#kg-left-sidebar-anchor),
            [data-testid="stHeader"],
            .kg-sidebar-resizer,
            .kg-askme-resizer,
            .kg-split-resizer,
            .kg-no-print {{
                display: none !important;
            }}
            .kg-report-paper {{
                border: none !important;
                box-shadow: none !important;
                padding: 0 !important;
                max-width: 100% !important;
            }}
        }}
    </style>
    """
    compact_css = "\n".join(line for line in css.splitlines() if line.strip())
    st.markdown(compact_css, unsafe_allow_html=True)
    return t


def escape_text(value: object) -> str:
    """Safely HTML-escape arbitrary text prior to template rendering."""
    return html.escape("" if value is None else str(value))

