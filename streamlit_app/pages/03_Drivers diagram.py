# pages/03_Drivers diagram.py
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Drivers Diagram", page_icon="🧩", layout="wide")

st.title("Drivers Diagram — Interrelations across Dimensions")
st.caption("Interactive schematic of drivers in four dimensions (conceptual). Hover to explore relationships.")

# ------------------------------------------------------------
# Sidebar options
# ------------------------------------------------------------
with st.sidebar:
    st.header("Display")
    show_labels = st.checkbox("Show node labels", value=True)
    arrow_width = st.slider("Arrow width", 1, 5, 3)
    curve = st.slider("Arrow curvature", 0.05, 0.4, 0.18)
    arrow_size = st.slider("Arrow head size", 0.6, 1.6, 1.0)

# ------------------------------------------------------------
# Node definitions
# ------------------------------------------------------------
DIM = {
    "Social": {
        "color": "#ff69b4", "text": "SOCIAL",
        "box": (6, 58, 42, 96),
        "nodes": [
            ("Social Networks", (24, 84)),
            ("Community participation", (24, 70)),
        ],
    },
    "Psychological": {
        "color": "#f39c12", "text": "Psychological",
        "box": (6, 6, 42, 46),
        "nodes": [
            ("Emotional security", (24, 40)),
            ("Sense of autonomy", (24, 30)),
            ("Purpose", (24, 20)),
            ("Downshift", (24, 10)),
        ],
    },
    "Environmental": {
        "color": "#27ae60", "text": "ENVIRONMENTAL",
        "box": (58, 56, 96, 96),
        "nodes": [
            ("Proximity to services", (77, 88)),
            ("Green spaces", (77, 80)),
            ("Mobility & Accessibility", (77, 72)),
            ("Social infrastructures", (77, 64)),
            ("Safety", (77, 58)),
        ],
    },
    "Physical": {
        "color": "#3498db", "text": "Physical",
        "box": (58, 6, 96, 46),
        "nodes": [
            ("Physical activity & active lifestyle", (77, 24)),
        ],
    },
}

node_pos, node_dim = {}, {}
for dim, cfg in DIM.items():
    for label, (x, y) in cfg["nodes"]:
        node_pos[label] = (x, y)
        node_dim[label] = dim

# ------------------------------------------------------------
# Edge definitions
# ------------------------------------------------------------
EDGES = [
    ("Proximity to services", "Social Networks"),
    ("Green spaces", "Social Networks"),
    ("Green spaces", "Community participation"),
    ("Green spaces", "Physical activity & active lifestyle"),
    ("Mobility & Accessibility", "Social Networks"),
    ("Mobility & Accessibility", "Community participation"),
    ("Mobility & Accessibility", "Physical activity & active lifestyle"),
    ("Social infrastructures", "Community participation"),
    ("Safety", "Social Networks"),
    ("Safety", "Community participation"),
    ("Emotional security", "Community participation"),
    ("Sense of autonomy", "Community participation"),
    ("Purpose", "Community participation"),
    ("Downshift", "Physical activity & active lifestyle"),
]

# ------------------------------------------------------------
# Build figure
# ------------------------------------------------------------
fig = go.Figure()

# Boxes
for dim, cfg in DIM.items():
    x0, y0, x1, y1 = cfg["box"]
    fig.add_shape(
        type="rect", x0=x0, y0=y0, x1=x1, y1=y1,
        line=dict(color=cfg["color"], width=2),
        fillcolor="rgba(0,0,0,0)", layer="below"
    )
    fig.add_annotation(
        x=x0 + 2, y=y1 - 2, text=f"<b>{cfg['text']}</b>",
        showarrow=False, font=dict(color=cfg["color"], size=14),
        xanchor="left", yanchor="top"
    )

# Curved arrows
for src, tgt in EDGES:
    x0, y0 = node_pos[src]
    x1, y1 = node_pos[tgt]

    # curvature midpoint
    mx = (x0 + x1) / 2
    my = (y0 + y1) / 2 + (x1 - x0) * curve  # adds curvature

    # draw as 3-point bezier approximation
    fig.add_trace(go.Scatter(
        x=[x0, mx, x1], y=[y0, my, y1],
        mode="lines",
        line=dict(color="#4CAF50", width=arrow_width, shape="spline", smoothing=1.3),
        hoverinfo="none"
    ))
    # add arrowhead manually
    fig.add_annotation(
        x=x1, y=y1, ax=mx, ay=my,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=3, arrowsize=arrow_size,
        arrowwidth=arrow_width, arrowcolor="#4CAF50"
    )

# Nodes
xs, ys, texts, colors, sizes = [], [], [], [], []
for label, (x, y) in node_pos.items():
    xs.append(x)
    ys.append(y)
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
    height=640,
    margin=dict(l=10, r=10, t=20, b=10),
    plot_bgcolor="white",
    xaxis=dict(range=[0, 100], visible=False),
    yaxis=dict(range=[0, 100], visible=False),
    showlegend=False,
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("About this diagram"):
    st.markdown("""
- **Curved arrows** visualize influences between dimensions.
- **Colors** group related drivers:
  - 🩷 Social 🟧 Psychological 🟩 Environmental 🩵 Physical
- Hover nodes to read their labels.
- The layout approximates the conceptual model for Ede–Veldhuizen.
""")
