# pages/03_Drivers diagram.py
import streamlit as st
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Drivers Diagram", page_icon="🧩", layout="wide")

st.title("Drivers Diagram — Interrelations across Dimensions")
st.caption("Interactive schematic of drivers in four dimensions. Colors = source dimension of each arrow.")

# ---------------- Sidebar: display options ----------------
with st.sidebar:
    st.header("Display")
    show_labels = st.checkbox("Show node labels", value=True)
    show_boxes  = st.checkbox("Show dimension frames", value=True)
    arrow_w     = st.slider("Arrow width", 1, 5, 3)
    arrow_size  = st.slider("Arrow head size", 0.6, 1.4, 1.0)
    curvature   = st.slider("Curvature", 0.08, 0.35, 0.18)

# ---------------- Dimensions, nodes (fixed layout) ----------------
# Canvas range widened a bit to create breathing room
XMIN, XMAX, YMIN, YMAX = 0, 112, 0, 100

DIM = {
    "Social": {
        "color": "#ff69b4", "label": "SOCIAL",
        "box": (6, 58, 42, 96),
        "nodes": [
            ("Social Networks",         (24, 84)),
            ("Community participation", (24, 66)),   # slightly lower for spacing
        ],
    },
    "Psychological": {
        "color": "#f39c12", "label": "Psychological",
        "box": (6, 6, 42, 46),
        "nodes": [
            ("Emotional security", (24, 40)),
            ("Sense of autonomy",  (24, 30)),
            ("Purpose",            (24, 20)),
            ("Downshift",          (24, 10)),
        ],
    },
    "Environmental": {
        "color": "#27ae60", "label": "ENVIRONMENTAL",
        # shifted right to reduce crossings
        "box": (66, 56, 108, 96),
        "nodes": [
            ("Proximity to services",     (90, 88)),
            ("Green spaces",              (90, 80)),
            ("Mobility & Accessibility",  (90, 72)),
            ("Social infrastructures",    (90, 64)),
            ("Safety",                    (90, 58)),
        ],
    },
    "Physical": {
        "color": "#3498db", "label": "Physical",
        # shifted right to match Environmental spacing
        "box": (66, 6, 108, 46),
        "nodes": [
            ("Physical activity & active lifestyle", (90, 24)),
        ],
    },
}

# Build lookups
node_pos, node_dim = {}, {}
for dim, cfg in DIM.items():
    for label, (x, y) in cfg["nodes"]:
        node_pos[label] = (x, y)
        node_dim[label] = dim

# ---------------- Directed edges (source, target) ----------------
# Match your figure; add more as needed
EDGES = [
    # Environmental → Social / Physical
    ("Proximity to services",        "Social Networks"),
    ("Green spaces",                 "Social Networks"),
    ("Green spaces",                 "Community participation"),
    ("Green spaces",                 "Physical activity & active lifestyle"),
    ("Mobility & Accessibility",     "Social Networks"),
    ("Mobility & Accessibility",     "Community participation"),
    ("Mobility & Accessibility",     "Physical activity & active lifestyle"),
    ("Social infrastructures",       "Community participation"),
    ("Safety",                       "Social Networks"),
    ("Safety",                       "Community participation"),
    # Psychological → Social / Physical
    ("Emotional security",           "Community participation"),
    ("Sense of autonomy",            "Community participation"),
    ("Purpose",                      "Community participation"),
    ("Downshift",                    "Physical activity & active lifestyle"),
]

# Arrow colors by SOURCE dimension
ARROW_COLORS = {
    "Environmental": "#27ae60",   # green
    "Psychological": "#f39c12",   # orange
    "Social": "#ff69b4",          # pink (unused now, but future-proof)
    "Physical": "#3498db",
}

# ---------------- Figure ----------------
fig = go.Figure()

# Frames (dimension boxes)
if show_boxes:
    for dim, cfg in DIM.items():
        x0, y0, x1, y1 = cfg["box"]
        fig.add_shape(
            type="rect", x0=x0, y0=y0, x1=x1, y1=y1,
            line=dict(color=cfg["color"], width=2),
            fillcolor="rgba(0,0,0,0)", layer="below"
        )
        fig.add_annotation(
            x=x0 + 2, y=y1 - 2, text=f"<b>{cfg['label']}</b>",
            showarrow=False, font=dict(color=cfg["color"], size=14),
            xanchor="left", yanchor="top"
        )

# Helper to draw a smooth curved link with arrowhead
def draw_curved_arrow(x0, y0, x1, y1, color):
    # Compute a control point that bows the line gently.
    # Curvature sign chosen so left→right curves arch slightly downward or upward based on vertical gap.
    dx, dy = x1 - x0, y1 - y0
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    ctrl_sign = 1 if dy < 0 else -1
    # Scale curvature by horizontal span (works for vertical-ish links too)
    offset = curvature * max(abs(dx), 16)
    cx, cy = mx, my + ctrl_sign * offset

    # Draw the spline (3 points approximated as a smooth line)
    fig.add_trace(go.Scatter(
        x=[x0, cx, x1], y=[y0, cy, y1],
        mode="lines",
        line=dict(color=color, width=arrow_w, shape="spline", smoothing=1.2),
        hoverinfo="none"
    ))
    # Arrowhead aimed from control point to target
    fig.add_annotation(
        x=x1, y=y1, ax=cx, ay=cy,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=3, arrowsize=arrow_size,
        arrowwidth=arrow_w, arrowcolor=color
    )

# Draw edges with small nudges so arrows don’t pierce node centers
for src, tgt in EDGES:
    x0, y0 = node_pos[src]
    x1, y1 = node_pos[tgt]
    color = ARROW_COLORS.get(node_dim[src], "#4CAF50")

    # Nudge start/end a bit along x depending on direction
    nudge = 1.2
    if x1 > x0:
        x0n, x1n = x0 + nudge, x1 - nudge
    else:
        x0n, x1n = x0 - nudge, x1 + nudge

    # For near-vertical edges, still add a tiny horizontal separation
    if abs(x1 - x0) < 6:
        x0n += -nudge
        x1n += nudge

    draw_curved_arrow(x0n, y0, x1n, y1, color)

# Draw nodes
xs, ys, texts, colors, sizes = [], [], [], [], []
for label, (x, y) in node_pos.items():
    xs.append(x); ys.append(y)
    texts.append(label if show_labels else "")
    colors.append(DIM[node_dim[label]]["color"])
    sizes.append(22 if node_dim[label] != "Physical" else 26)

fig.add_trace(go.Scatter(
    x=xs, y=ys,
    mode="markers+text" if show_labels else "markers",
    text=texts,
    textposition="middle left",
    marker=dict(size=sizes, color=colors, line=dict(width=2, color="white")),
    hovertemplate="<b>%{text}</b><extra></extra>"
))

# Layout
fig.update_layout(
    height=660,
    margin=dict(l=10, r=10, t=20, b=10),
    plot_bgcolor="white",
    xaxis=dict(range=[XMIN, XMAX], visible=False),
    yaxis=dict(range=[YMIN, YMAX], visible=False),
    showlegend=False,
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("About this diagram"):
    st.markdown("""
- **Colors on arrows = source dimension** (🟩 Environmental, 🟧 Psychological, 🩷 Social if used, 🩵 Physical).
- Curved links reduce overlap and echo the conceptual flow in your report.
- Positions are fixed so it mirrors the figure; tweak any `(x, y)` in the `DIM[...]` blocks to nudge nodes.
- Add or remove relationships by editing the `EDGES` list.
""")
