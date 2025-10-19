# pages/04_Scenarios.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Page config MUST be the first Streamlit call
st.set_page_config(page_title="Scenarios • Veldhuizen", layout="wide")

st.subheader("Concept demo — Simulation of scenarios")
st.caption("Mock relationships for illustration only. Adjust benches and see how dimensions and QoL change.")

# ------------------------------------------------------------
# Controls (presets + slider)
# ------------------------------------------------------------
col_p1, col_p2, col_p3 = st.columns(3)
if "bench_delta" not in st.session_state:
    st.session_state.bench_delta = 0

with col_p1:
    if st.button("Baseline (0)"):
        st.session_state.bench_delta = 0
with col_p2:
    if st.button("+5 benches"):
        st.session_state.bench_delta = 5
with col_p3:
    if st.button("-5 benches"):
        st.session_state.bench_delta = -5

b = st.slider("Benches (add/remove)", -10, 10, st.session_state.bench_delta)
st.session_state.bench_delta = b  # keep slider + presets in sync
st.caption("Legend: solid green arrow = positive effect; dashed red arrow = negative effect.")

# ------------------------------------------------------------
# Mock relationships (logic unchanged)
# ------------------------------------------------------------
# Per-bench effects on factors
d_social   =  2 * b        # +2 per bench
d_physical =  1 * b        # +1 per bench
d_safety   = -2 * b        # −2 per bench (e.g., perceived nuisance)

# Dimension → QoL weights (so +1 bench → +4, +2, −4)
W_SOC, W_PHY, W_ENV = 2, 2, 2
q_social   = W_SOC * d_social
q_physical = W_PHY * d_physical
q_env      = W_ENV * d_safety
q_total    = q_social + q_physical + q_env

def plus(v):
    return f"{int(v):+d}" if isinstance(v, (int, np.integer)) else f"{v:+.0f}"

# ------------------------------------------------------------
# Diagram layout (polished visuals)
# ------------------------------------------------------------
# Canvas coordinates (0..10)
bench_x, bench_y = 1.3, 5.0
soc_x, soc_y     = 4.2, 8.2
phy_x, phy_y     = 4.2, 5.0
env_x, env_y     = 4.2, 1.8
qol_x, qol_y     = 9.0, 5.0

# Bubble / card sizes
oval_w, oval_h = 3.8, 2.2
card_w, card_h = 2.2, 1.0

# Visual styling
FONT = "Inter, Segoe UI, system-ui, -apple-system, sans-serif"

# Color system
COL_POS = "#2ecc71"   # positive (arrows)
COL_NEG = "#e74c3c"   # negative (arrows)
COL_NEU = "#7f8c8d"

SOC_COL, SOC_BG, SOC_OUT = "#e67e22", "#fdf2e9", "#fad7a0"
PHY_COL, PHY_BG, PHY_OUT = "#2980b9", "#eaf2fb", "#aed6f1"
ENV_COL, ENV_BG, ENV_OUT = "#8e44ad", "#f7e9fd", "#d7bde2"
Q_BG, Q_BR               = "#eafaf1", "#2ecc71"
BENCH_BG, BENCH_BR       = "#f4d03f", "#b7950b"

def arrow_style(delta):
    stl = dict(
        showarrow=True, arrowhead=3, arrowsize=1.1, arrowwidth=3,
        arrowcolor=(COL_POS if delta > 0 else COL_NEG if delta < 0 else COL_NEU),
        standoff=2,
    )
    if delta < 0:
        stl["dash"] = "dash"
    return stl

fig = go.Figure()

# Bench block
fig.add_shape(
    type="rect",
    x0=bench_x - 1.5, y0=bench_y - 1.0, x1=bench_x + 1.5, y1=bench_y + 1.0,
    fillcolor=BENCH_BG, line=dict(color=BENCH_BR, width=2), layer="below"
)
bench_label = f"<b>{plus(b)}</b> bench{'es' if abs(b) != 1 else ''}" if b != 0 else "<b>±0</b> benches"
fig.add_annotation(
    x=bench_x, y=bench_y, text=bench_label, showarrow=False,
    font=dict(size=16, family=FONT, color="#3a3a3a")
)

# Helpers to draw a “bubble” panel + card label
def bubble(x, y, w, h, title, tcolor, bg, outline):
    fig.add_shape(
        type="circle", x0=x - w/2, y0=y - h/2, x1=x + w/2, y1=y + h/2,
        fillcolor=bg, line=dict(color=outline, width=2, dash="dot"), layer="below"
    )
    fig.add_annotation(
        x=x, y=y + h/2 - 0.2, text=f"<b>{title}</b>", yshift=10,
        showarrow=False, font=dict(size=13, family=FONT, color=tcolor)
    )

def pill(x, y, txt, line_color):
    fig.add_shape(
        type="rect", x0=x - card_w/2, y0=y - card_h/2, x1=x + card_w/2, y1=y + card_h/2,
        fillcolor="white", line=dict(color=line_color, width=2)
    )
    fig.add_annotation(
        x=x, y=y, text=txt, showarrow=False,
        font=dict(size=12, family=FONT, color=line_color)
    )

# Social
bubble(soc_x, soc_y, oval_w, oval_h, "Social dimension", SOC_COL, SOC_BG, SOC_OUT)
pill(soc_x,  soc_y,  f"<b>{plus(d_social)}</b>&nbsp; Social interactions", SOC_COL)

# Physical
bubble(phy_x, phy_y, oval_w, oval_h, "Physical dimension", PHY_COL, PHY_BG, PHY_OUT)
pill(phy_x,  phy_y,  f"<b>{plus(d_physical)}</b>&nbsp; Physical activity",  PHY_COL)

# Environmental
bubble(env_x, env_y, oval_w, oval_h, "Environmental dimension", ENV_COL, ENV_BG, ENV_OUT)
pill(env_x,  env_y,  f"<b>{plus(d_safety)}</b>&nbsp; Safety", ENV_COL)

# QoL box
fig.add_shape(
    type="rect",
    x0=qol_x - 2.0, y0=qol_y - 1.6, x1=qol_x + 2.0, y1=qol_y + 1.6,
    fillcolor=Q_BG, line=dict(color=Q_BR, width=3)
)
qol_text = (
    f"<b>Δ QoL</b><br>"
    f"{plus(q_social)} from Social<br>"
    f"{plus(q_physical)} from Physical<br>"
    f"{plus(q_env)} from Environmental"
)
fig.add_annotation(
    x=qol_x, y=qol_y, text=qol_text, showarrow=False,
    font=dict(size=13, family=FONT, color="#2d3436")
)

# Bench → factors
fig.add_annotation(x=soc_x - 1.15, y=soc_y, ax=bench_x + 1.55, ay=bench_y, **arrow_style(d_social))
fig.add_annotation(x=phy_x - 1.15, y=phy_y, ax=bench_x + 1.55, ay=bench_y, **arrow_style(d_physical))
fig.add_annotation(x=env_x - 1.15, y=env_y, ax=bench_x + 1.55, ay=bench_y, **arrow_style(d_safety))

# Factors → QoL (use positive-colored arrows to the right box; sign is in numbers)
arrow_to_qol = dict(showarrow=True, arrowhead=3, arrowsize=1.2, arrowwidth=3, arrowcolor=COL_POS)
x_q_target = (qol_x - 2.0) + 0.08
fig.add_annotation(x=x_q_target, y=qol_y + 1.1, ax=soc_x + card_w/2, ay=soc_y, **arrow_to_qol)
fig.add_annotation(x=x_q_target, y=phy_y,      ax=phy_x + card_w/2, ay=phy_y, **arrow_to_qol)
fig.add_annotation(x=x_q_target, y=qol_y - 1.1, ax=env_x + card_w/2, ay=env_y, **arrow_to_qol)

# Mini legend
LEG_X, LEG_Y = 6.1, 9.4
fig.add_annotation(x=LEG_X, y=LEG_Y, text="<b>Legend</b>", showarrow=False,
                   font=dict(size=12, family=FONT, color="#2d3436"))
fig.add_annotation(x=LEG_X - 0.1, y=LEG_Y - 0.35, ax=LEG_X - 1.0, ay=LEG_Y - 0.35,
                   showarrow=True, arrowcolor=COL_POS, arrowwidth=3, arrowsize=1, arrowhead=3)
fig.add_annotation(x=LEG_X + 1.25, y=LEG_Y - 0.35, text="Positive effect", showarrow=False,
                   font=dict(size=11, family=FONT, color="#2d3436"))
fig.add_annotation(x=LEG_X - 0.1, y=LEG_Y - 0.75, ax=LEG_X - 1.0, ay=LEG_Y - 0.75,
                   showarrow=True, arrowcolor=COL_NEG, arrowwidth=3, arrowsize=1, arrowhead=3, dash="dash")
fig.add_annotation(x=LEG_X + 1.25, y=LEG_Y - 0.75, text="Negative effect", showarrow=False,
                   font=dict(size=11, family=FONT, color="#2d3436"))

# Axes + layout
fig.update_xaxes(visible=False, range=[0, 11])
fig.update_yaxes(visible=False, range=[0, 10])
fig.update_layout(
    template="plotly_white",
    height=560,
    margin=dict(l=24, r=24, t=24, b=18),
    font=dict(family=FONT, size=13, color="#2d3436"),
)

# ------------------------------------------------------------
# Compact KPIs + small QoL gauge
# ------------------------------------------------------------
BASE_QOL = 70
qol_after = float(np.clip(BASE_QOL + q_total, 0, 100))

g = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=qol_after,
    number={"suffix": " / 100"},
    delta={"reference": BASE_QOL,
           "increasing": {"color": "#27ae60"},
           "decreasing": {"color": "#c0392b"}},
    gauge={"axis": {"range": [0, 100]},
           "bar": {"color": "#34495e"},
           "steps": [{"range": [0, 40]}, {"range": [40, 70]}, {"range": [70, 100]}]},
    title={"text": "QoL index (mock)"},
))
g.update_layout(height=220, margin=dict(l=10, r=10, t=30, b=10), template="plotly_white")

# ------------------------------------------------------------
# Page layout: diagram left, KPIs/gauge right
# ------------------------------------------------------------
try:
    left, right = st.columns([3, 1.7], vertical_alignment="top")
except TypeError:  # older Streamlit versions
    left, right = st.columns([3, 1.7])

with left:
    st.plotly_chart(fig, use_container_width=True)

with right:
    c1, c2 = st.columns(2)
    c1.metric("Δ Social interactions",   plus(d_social))
    c2.metric("Δ Physical activity",     plus(d_physical))
    st.metric("Δ Safety",                plus(d_safety))
    st.metric("Δ QoL (composite)",      plus(q_total))
    st.plotly_chart(g, use_container_width=True)

# ------------------------------------------------------------
# Notes
# ------------------------------------------------------------
with st.expander("Notes (prototype logic)"):
    st.markdown("""
- Per bench effects (mock): **+2 Social interactions**, **+1 Physical activity**, **−2 Safety**.
- Dimensions contribute to QoL with equal weights (2, 2, 2) → for +1 bench: **+4**, **+2**, **−4**.
- This is a **conceptual** demo to communicate relationships, not a predictive model.
""")
