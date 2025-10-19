# pages/03_Drivers diagram.py
import streamlit as st
import plotly.graph_objects as go

# Page config first
st.set_page_config(page_title="Drivers Diagram", page_icon="🧩", layout="wide")

st.title("Drivers Diagram — Interrelations across Dimensions")
st.caption("Interactive schematic of drivers in four dimensions (conceptual). Hover nodes; toggle edges in the sidebar.")

# ------------------------------------------------------------
# Sidebar: simple display options
# ------------------------------------------------------------
with st.sidebar:
    st.header("Display")
    show_labels = st.checkbox("Show node labels", value=True)
    show_boxes  = st.checkbox("Show dimension boxes", value=True)
    arrow_width = st.slider("Arrow width", 1, 6, 3)
    arrow_size  = st.slider("Arrow head size", 0.6, 1.6, 1.0)

# ------------------------------------------------------------
# Nodes (by dimension) — positions are fixed to mirror your diagram
# Canvas coordinates: x∈[0,100], y∈[0,100]
# ------------------------------------------------------------
DIM = {
    "Social": {
        "color": "#ff69b4", "text": "SOCIAL",
        "box": (6, 56, 42, 96),  # x0,y0,x1,y1
        "nodes": [
            ("Social Networks",           (24, 84)),
            ("Community participation",   (24, 70)),
        ],
    },
    "Psychological": {
        "color": "#f39c12", "text": "Psychological",
        "box": (6, 6, 42, 46),
        "nodes": [
            ("Emotional security", (24, 40)),
            ("Sense of autonomy",  (24, 30)),
            ("Purpose",            (24, 20)),
            ("Downshift",          (24, 10)),
        ],
    },
    "Environmental": {
        "color": "#27ae60", "text": "ENVIRONMENTAL",
        "box": (58, 56, 96, 96),
        "nodes": [
            ("Proximity to services", (77, 88)),
            ("Green spaces",          (77, 80)),
            ("Mobility & Accessibility",(77, 72)),
            ("Social infrastructures",(77, 64)),
            ("Safety",                (77, 58)),
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

# Build a lookup of all node positions + their dimension color
node_pos = {}
node_dim = {}
for dim, cfg in DIM.items():
    for label, (x, y) in cfg["nodes"]:
        node_pos[label] = (x, y)
        node_dim[label] = dim

# ------------------------------------------------------------
# Edges (directed) — based on the relationships in your figure
# You can extend/modify freely; each item is (source, target)
# ------------------------------------------------------------
EDGES = [
    # Environmental -> Social + Physical
    ("Proximity to services", "Social Networks"),
    ("Proximity to services", "Community participation"),
    ("Green spaces", "Social Networks"),
    ("Green spaces", "Community participation"),
    ("Green spaces", "Physical activity & active lifestyle"),
    ("Mobility & Accessibility", "Social Networks"),
    ("Mobility & Accessibility", "Community participation"),
    ("Mobility & Accessibility", "Physical activity & active lifestyle"),
    ("Social infrastructures", "Community participation"),
    ("Safety", "Social Networks"),
    ("Safety", "Community participation"),
    # Psychological -> Social / Physical
    ("Emotional security", "Community participation"),
    ("Sense of autonomy", "Community participation"),
    ("Purpose", "Community participation"),
    ("Downshift", "Physical activity & active lifestyle"),
]

# ------------------------------------------------------------
# Figure setup
# ------------------------------------------------------------
fig = go.Figure()

# Dimension rounded rectangles (optional)
if show_boxes:
    for dim, cfg in DIM.items():
        x0, y0, x1, y1 = cfg["box"]
        fig.add_shape(
            type="rect", x0=x0, y0=y0, x1=x1, y1=y1,
            line=dict(color=cfg["color"], width=2),
            fillcolor=f"rgba(0,0,0,0)",  # hollow
            layer="below"
        )
        # Title label on the side of each box
        fig.add_annotation(
            x=x0+2, y=y1-2, text=f"<b>{cfg['text']}</b>",
            showarrow=False, font=dict(color=cfg["color"], size=14), xanchor="left", yanchor="top"
        )

# Draw arrows as annotations (gives us true arrowheads)
for src, tgt in EDGES:
    x0, y0 = node_pos[src]
    x1, y1 = node_pos[tgt]

    # small nudges so arrows don't overlap node markers
    dx = 1.2 if x1 > x0 else -1.2
    dy = 0.0
    fig.add_annotation(
        x=x1 - dx, y=y1 - dy,  # arrow tip (near target)
        ax=x0 + dx, ay=y0 + dy,  # arrow tail (near source)
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=3, arrowsize=arrow_size, arrowwidth=arrow_width,
        arrowcolor="#4CAF50",
    )

# Draw nodes
xs, ys, texts, colors, sizes = [], [], [], [], []
for label, (x, y) in node_pos.items():
    xs.append(x); ys.append(y)
    texts.append(label if show_labels else "")
    colors.append(DIM[node_dim[label]]["color"])
    sizes.append(22 if node_dim[label] != "Physical" else 26)

fig.add_trace(go.Scatter(
    x=xs, y=ys, mode="markers+text" if show_labels else "markers",
    text=texts, textposition="middle left",
    marker=dict(size=sizes, color=colors, line=dict(width=2, color="white")),
    hovertemplate="<b>%{text}</b><extra></extra>" if show_labels else "<extra></extra>"
))

# Aesthetics
fig.update_layout(
    height=640, margin=dict(l=10, r=10, t=20, b=10),
    showlegend=False, plot_bgcolor="white",
    xaxis=dict(range=[0, 100], visible=False), yaxis=dict(range=[0, 100], visible=False),
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("About this diagram"):
    st.markdown("""
- This is a **conceptual** map of interrelations between drivers in four dimensions.
- Arrows indicate the direction of influence (from source to target).
- Colors group drivers by dimension:
  - **Pink** Social, **Orange** Psychological, **Green** Environmental, **Blue** Physical.
- Positions are fixed to mirror the report figure (not a force-directed layout).
""")
