"""Interactive Plotly + NetworkX knowledge graph helpers styled for Obsidian and Limestone."""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Set, Tuple

import networkx as nx
import plotly.graph_objects as go

from KnowledgeGraphAI.frontend.components.theme import (
    ENTITY_PALETTES,
    get_entity_color,
    get_tokens,
)

# Preserve CATEGORY_COLORS constant for backwards compatibility
CATEGORY_COLORS: Dict[str, str] = dict(ENTITY_PALETTES["obsidian"])


def filter_subgraph(
    graph_json: Dict[str, Any],
    *,
    selected_categories: Optional[List[str]] = None,
    focus_node_id: Optional[str] = None,
    search_query: Optional[str] = None,
    max_nodes: int = 45,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Filter document graph by categories, search query, focus node ego-network, and max node cap."""
    nodes = list(graph_json.get("nodes") or [])
    edges = list(graph_json.get("edges") or [])
    if not nodes:
        return [], []

    allowed_cats = set(selected_categories) if selected_categories else None
    node_map = {n["id"]: n for n in nodes if n.get("id")}

    candidate_ids: Set[str] = set()
    query = (search_query or "").strip().lower()

    if focus_node_id and focus_node_id in node_map:
        candidate_ids.add(focus_node_id)
        for edge in edges:
            src = edge.get("source")
            dst = edge.get("target")
            if src == focus_node_id and dst in node_map:
                candidate_ids.add(dst)
            elif dst == focus_node_id and src in node_map:
                candidate_ids.add(src)
    elif query:
        matched_ids: Set[str] = set()
        for node in nodes:
            label_match = query in str(node.get("label") or "").lower()
            alias_match = any(query in str(a).lower() for a in (node.get("aliases") or []))
            cat_match = query in str(node.get("category") or "").lower()
            if label_match or alias_match or cat_match:
                matched_ids.add(node["id"])
        candidate_ids.update(matched_ids)
        for edge in edges:
            src = edge.get("source")
            dst = edge.get("target")
            if src in matched_ids and dst in node_map:
                candidate_ids.add(dst)
            elif dst in matched_ids and src in node_map:
                candidate_ids.add(src)
    else:
        candidate_ids = set(node_map.keys())

    filtered_nodes = [
        node_map[nid]
        for nid in candidate_ids
        if nid in node_map
        and (
            allowed_cats is None
            or node_map[nid].get("category") in allowed_cats
            or nid == focus_node_id
        )
    ]
    filtered_nodes.sort(
        key=lambda n: (
            1 if n.get("id") == focus_node_id else 0,
            n.get("degree", 0),
            n.get("occurrences", 0),
        ),
        reverse=True,
    )
    filtered_nodes = filtered_nodes[: max(5, max_nodes)]
    kept_ids = {n["id"] for n in filtered_nodes}
    filtered_edges = [
        e for e in edges if e.get("source") in kept_ids and e.get("target") in kept_ids
    ]
    return filtered_nodes, filtered_edges


def build_interactive_figure(
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    *,
    selected_node_id: Optional[str] = None,
    theme_name: str = "obsidian",
    view_revision: str = "default",
) -> Tuple[go.Figure, List[str]]:
    """Build a crisp Industrial / Architectural Plotly knowledge graph with directional arrows.

    Returns (figure, flat_node_ids) in the exact point sequence of node traces so
    Streamlit `on_select` click indices map deterministically back to node IDs.
    """
    t = get_tokens(theme_name)
    fig = go.Figure()

    if not nodes:
        fig.update_layout(
            height=540,
            paper_bgcolor=t["graph_bg"],
            plot_bgcolor=t["graph_bg"],
            xaxis={"visible": False},
            yaxis={"visible": False},
            annotations=[
                {
                    "text": "No graph nodes match the active category or search filter.",
                    "xref": "paper",
                    "yref": "paper",
                    "x": 0.5,
                    "y": 0.5,
                    "showarrow": False,
                    "font": {"color": t["text_secondary"], "size": 14, "family": "Inter, sans-serif"},
                }
            ],
        )
        return fig, []

    graph = nx.DiGraph()
    for node in nodes:
        graph.add_node(node["id"])
    for edge in edges:
        graph.add_edge(edge["source"], edge["target"], relation=edge.get("relation", "RELATES_TO"))

    undirected = graph.to_undirected()
    n_count = len(nodes)
    components = sorted(nx.connected_components(undirected), key=len, reverse=True)
    pos: Dict[str, Tuple[float, float]] = {}

    if len(components) <= 1:
        spacing_k = 1.9 / math.sqrt(max(n_count, 2))
        raw_pos = nx.spring_layout(undirected, k=spacing_k, iterations=120, seed=42)
        pos = {nid: (float(xy[0]), float(xy[1])) for nid, xy in raw_pos.items()}
    else:
        # Layout giant connected component centrally, place satellite nodes/components tidily nearby
        main_nodes = list(components[0])
        main_sub = undirected.subgraph(main_nodes)
        main_raw = nx.spring_layout(main_sub, k=1.8 / math.sqrt(max(len(main_nodes), 2)), iterations=120, seed=42)
        for nid, xy in main_raw.items():
            pos[nid] = (float(xy[0]) * 0.78, float(xy[1]) * 0.78)

        sat_nodes = [nid for comp in components[1:] for nid in comp]
        sat_count = len(sat_nodes)
        for idx, nid in enumerate(sat_nodes):
            angle = (2.0 * math.pi * idx) / max(sat_count, 1)
            pos[nid] = (1.05 * math.cos(angle), 0.92 * math.sin(angle))

    # Rescale coordinates safely inside [-0.95, 0.95] so edge labels never clip at margins
    if pos:
        all_x = [p[0] for p in pos.values()]
        all_y = [p[1] for p in pos.values()]
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        span_x = max(max_x - min_x, 1e-4)
        span_y = max(max_y - min_y, 1e-4)
        cx = (min_x + max_x) / 2.0
        cy = (min_y + max_y) / 2.0
        pos = {
            nid: (
                ((xy[0] - cx) / span_x) * 1.75 if len(pos) > 1 else 0.0,
                ((xy[1] - cy) / span_y) * 1.75 if len(pos) > 1 else 0.0,
            )
            for nid, xy in pos.items()
        }

    # Identify connected neighbors when a node is selected
    neighbor_ids: Set[str] = set()
    active_edges: List[Dict[str, Any]] = []
    dim_edges: List[Dict[str, Any]] = []
    if selected_node_id and selected_node_id in pos:
        neighbor_ids.add(selected_node_id)
        for edge in edges:
            src, dst = edge.get("source"), edge.get("target")
            if src == selected_node_id or dst == selected_node_id:
                active_edges.append(edge)
                if src:
                    neighbor_ids.add(src)
                if dst:
                    neighbor_ids.add(dst)
            else:
                dim_edges.append(edge)
    else:
        active_edges = list(edges)

    def _edge_segments(edge_list: List[Dict[str, Any]]) -> Tuple[List[Optional[float]], List[Optional[float]]]:
        xs: List[Optional[float]] = []
        ys: List[Optional[float]] = []
        for edge in edge_list:
            src, dst = edge.get("source"), edge.get("target")
            if src not in pos or dst not in pos:
                continue
            x0, y0 = pos[src]
            x1, y1 = pos[dst]
            xs.extend([float(x0), float(x1), None])
            ys.extend([float(y0), float(y1), None])
        return xs, ys

    # Dim background edges when selection is active
    if dim_edges:
        dim_x, dim_y = _edge_segments(dim_edges)
        fig.add_trace(
            go.Scatter(
                x=dim_x,
                y=dim_y,
                mode="lines",
                line={"width": 1.1, "color": t["graph_edge_dim"]},
                hoverinfo="none",
                showlegend=False,
                name="Context Edges",
            )
        )

    # Active / primary edges
    if active_edges:
        act_x, act_y = _edge_segments(active_edges)
        edge_color = t["accent"] if selected_node_id else t["graph_edge"]
        edge_width = 2.0 if selected_node_id else 1.45
        fig.add_trace(
            go.Scatter(
                x=act_x,
                y=act_y,
                mode="lines",
                line={"width": edge_width, "color": edge_color},
                hoverinfo="none",
                showlegend=False,
                name="Relationships",
            )
        )

    # Edge midpoint hover markers for relationship tooltips
    mid_x: List[float] = []
    mid_y: List[float] = []
    mid_hover: List[str] = []
    arrows: List[Dict[str, Any]] = []
    max_arrows = 45

    for idx, edge in enumerate(edges):
        src, dst = edge.get("source"), edge.get("target")
        if src not in pos or dst not in pos:
            continue
        x0, y0 = pos[src]
        x1, y1 = pos[dst]
        mid_x.append((x0 + x1) / 2.0)
        mid_y.append((y0 + y1) / 2.0)
        rel_name = str(edge.get("relation") or "RELATES_TO").replace("_", " ")
        src_lbl = edge.get("source_label") or src
        dst_lbl = edge.get("target_label") or dst
        src_ref = edge.get("source_ref") or f"Page {edge.get('page_number', '?')}"
        conf = float(edge.get("confidence") or 0.0)
        mid_hover.append(
            f"<b>{src_lbl}</b> -> <i>{rel_name}</i> -> <b>{dst_lbl}</b>"
            f"<br>Confidence: {conf:.2f} | Source: {src_ref}"
        )

        is_highlighted = (not selected_node_id) or (src == selected_node_id or dst == selected_node_id)
        if is_highlighted and len(arrows) < max_arrows:
            dx = x1 - x0
            dy = y1 - y0
            dist = math.hypot(dx, dy)
            if dist > 1e-4:
                # Place crisp arrowhead cleanly before target node center
                shrink = min(0.16, dist * 0.25)
                tx = x1 - (dx / dist) * shrink
                ty = y1 - (dy / dist) * shrink
                sx = x1 - (dx / dist) * min(dist * 0.48, shrink + 0.14)
                sy = y1 - (dy / dist) * min(dist * 0.48, shrink + 0.14)
                arrows.append(
                    {
                        "x": float(tx),
                        "y": float(ty),
                        "ax": float(sx),
                        "ay": float(sy),
                        "xref": "x",
                        "yref": "y",
                        "axref": "x",
                        "ayref": "y",
                        "showarrow": True,
                        "arrowhead": 2,
                        "arrowsize": 1.05 if selected_node_id else 0.9,
                        "arrowwidth": 1.6 if selected_node_id else 1.2,
                        "arrowcolor": t["accent"] if selected_node_id else t["graph_edge"],
                        "opacity": 0.92 if selected_node_id else 0.72,
                    }
                )

    if mid_x:
        fig.add_trace(
            go.Scatter(
                x=mid_x,
                y=mid_y,
                mode="markers",
                marker={"size": 7, "color": "rgba(0,0,0,0)"},
                hoverinfo="text",
                hovertext=mid_hover,
                showlegend=False,
                name="Relationship Labels",
            )
        )

    # Group nodes by category; record deterministic node order for Plotly point selection
    by_category: Dict[str, List[Dict[str, Any]]] = {}
    for node in nodes:
        by_category.setdefault(str(node.get("category") or "Concept"), []).append(node)

    flat_node_ids: List[str] = []
    for category, cat_nodes in by_category.items():
        color = get_entity_color(category, theme_name)
        xs: List[float] = []
        ys: List[float] = []
        texts: List[str] = []
        hovers: List[str] = []
        sizes: List[float] = []
        opacities: List[float] = []
        line_widths: List[float] = []
        line_colors: List[str] = []

        for node in cat_nodes:
            nid = node["id"]
            flat_node_ids.append(nid)
            x, y = pos[nid]
            xs.append(float(x))
            ys.append(float(y))

            is_selected = nid == selected_node_id
            is_neighbor = (not selected_node_id) or (nid in neighbor_ids)

            label = str(node.get("label") or nid)
            # Show full labels for visible/important nodes, slightly concise if large graph
            display_label = label if (len(label) <= 22 or is_selected or n_count <= 25) else f"{label[:19]}..."
            texts.append(display_label if is_neighbor else "")

            deg = int(node.get("degree", 0))
            occ = int(node.get("occurrences", 1))
            base_size = 17 + min(18, deg * 2.3 + occ * 0.9)
            sizes.append(base_size + (7 if is_selected else 0))

            opacities.append(1.0 if is_neighbor else 0.28)
            line_widths.append(3.2 if is_selected else (1.8 if (selected_node_id and is_neighbor) else 1.3))
            line_colors.append(
                t["accent"]
                if is_selected
                else (t["text_primary"] if is_neighbor else t["border"])
            )

            aliases = ", ".join(node.get("aliases") or [])
            alias_row = f"<br>Aliases: {aliases}" if aliases else ""
            refs = ", ".join(node.get("source_refs") or []) or "Document text"
            hovers.append(
                f"<b>{label}</b> [{category}]"
                f"<br>Connections: {deg} | Mentions: {occ}"
                f"{alias_row}"
                f"<br>Sources: {refs}"
            )

        fig.add_trace(
            go.Scatter(
                x=xs,
                y=ys,
                mode="markers+text",
                name=category,
                text=texts,
                textposition="top center",
                textfont={
                    "size": 11 if n_count <= 30 else 10,
                    "color": t["text_primary"],
                    "family": "Inter, sans-serif",
                },
                hoverinfo="text",
                hovertext=hovers,
                customdata=cat_nodes,
                marker={
                    "size": sizes,
                    "color": color,
                    "opacity": opacities,
                    "line": {"width": line_widths, "color": line_colors},
                },
            )
        )

    fig.update_layout(
        autosize=True,
        height=560,
        margin={"l": 14, "r": 14, "t": 44, "b": 14},
        paper_bgcolor=t["graph_bg"],
        plot_bgcolor=t["graph_bg"],
        hovermode="closest",
        dragmode="pan",
        uirevision=view_revision,
        clickmode="event+select",
        annotations=arrows,
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "left",
            "x": 0.0,
            "font": {"color": t["text_primary"], "size": 11, "family": "Inter, sans-serif"},
            "bgcolor": "rgba(0,0,0,0)",
        },
        xaxis={
            "showgrid": True,
            "gridcolor": t["graph_grid"],
            "zeroline": False,
            "showticklabels": False,
            "range": [-1.28, 1.28],
        },
        yaxis={
            "showgrid": True,
            "gridcolor": t["graph_grid"],
            "zeroline": False,
            "showticklabels": False,
            "range": [-1.32, 1.32],
        },
    )
    return fig, flat_node_ids
