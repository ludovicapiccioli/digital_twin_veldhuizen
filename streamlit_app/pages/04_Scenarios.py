# pages/04_Scenarios.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Page config MUST be first Streamlit call in this file
st.set_page_config(page_title="Scenarios • Veldhuizen", layout="wide")

st.subheader("Concept demo - Simulation of scenarios")
st.caption("Concept demo with mock relationships. Adjust benches and see how dimensions and QoL change.")

# ------------------------------------------------------------
# Controls (minus / plus buttons + slider)
# ------------------------------------------------------------
MIN_B, MAX_B = -10, 10
if "bench_delta" not in st.session_state:
    st.session_state.bench_delta = 0

col_minus, col_value, col_plus = st.columns([1, 2, 1])

with col_minus:
    # Use emoji to guarantee rendering in the button
    if st.button("➖", use_container_width=True, key="btn_minus"):
        st.session_state.bench_delta = max(MIN_B, st.session_state.bench_delta - 1)

with col_value:
    st.markdown(
        f"<div style='text-align:center; font-size:22px; line-height:1.4'>"
        f"<b>{st.session_state.bench_delta:+d}</b> benches"
        f"</div>",
        unsafe_allow_html=True
    )

with col_plus:
    # Use emoji or full-width plus "＋" to avoid missing "+"
    if st.button("➕", use_container_width=True, key="btn_plus"):
        st.session_state.bench_delta = min(MAX_B, st.session_state.bench_delta + 1)

# Slider (stays in sync with buttons)
b = st.slider(
    "Benches (add/remove)",
    MIN_B, MAX_B, st.session_state.bench_delta, key="bench_slider"
)
if b != st.session_state.bench_delta:
    st.session_state.bench_delta = b
b = st.session_state.bench_delta  # use `b` below

# ------------------------------------------------------------
# Mock relationships
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

def sign_color(v):  # green for positive, red for negative, grey for zero
    return "#27ae60" if v > 0 else ("#c0392b" if v < 0 else "#7f8c8d")

def plus(v):        # format with sign
    return f"{int(v):+d}" if isinstance(v, (int, np.integer)) else f"{v:+.0f}"

# ------------------------------------------------------------
# Diagram layout (Plotly shapes & arrows)
# ------------------------------------------------------------
# Canvas coordinates (0..10 in both axes)
bench_x, bench_y = 1.3, 5.0
soc_x, soc_y     = 4.2, 8.2
phy_x, phy_y     = 4.2, 5.0
env_x, env_y     = 4.2, 1.8
qol_x, qol_y     = 9.0, 5.0

# Bubble / card sizes
oval_w, oval_h = 3.8, 2.2
card_w, card_h = 2.2, 1.0

# Colors
YELLOW  = "#f1c40f"
SOC_COL = "#e67e22"; SOC_BG = "#fce9e3"; SOC_OUT = "#fadbd8"
PHY_COL = "#2980b9"; PHY_BG = "#e8f1fb"; PHY_OUT = "#d6eaf8"
ENV_COL = "#8e44ad"; ENV_BG = "#f7e9f5"; ENV_OUT = "#f5eef8"
Q_BG    = "#b8e994"; Q_BR   = "#78e08f"
GREEN   = "#27ae60"

fig = go.Figure()

# Bench (left)
fig.add_shape(type="rect",
              x0=bench_x-1.4, y0=bench_y-0.9, x1=bench_x+1.4, y1=bench_y+0.9,
              fillcolor=YELLOW, line=dict(color="#b7950b", width=2), layer="below")
bench_label = f"<b>{plus(b)} Bench</b>" if b != 0 else "<b>±0 Bench</b>"
fig.add_annotation(x=bench_x, y=bench_y, text=bench_label, showarrow=False, font=dict(size=14))

# Social bubble + card
fig.add_shape(type="circle",
              x0=soc_x-oval_w/2, y0=soc_y-oval_h/2, x1=soc_x+oval_w/2, y1=soc_y+oval_h/2,
              fillcolor=SOC_BG, line=dict(color=SOC_OUT, width=2, dash="dash"), layer="below")
fig.add_annotation(x=soc_x, y=soc_y+oval_h/2-0.2, text="<b>Social dimension</b>",
                   showarrow=False, font=dict(color=SOC_COL, size=12), yshift=10)
fig.add_shape(type="rect",
              x0=soc_x-card_w/2, y0=soc_y-card_h/2, x1=soc_x+card_w/2, y1=soc_y+card_h/2,
              fillcolor="white", line=dict(color=SOC_COL, width=2))
fig.add_annotation(x=soc_x, y=soc_y,
                   text=f"<b>{plus(d_social)}</b>&nbsp; Social interactions",
                   showarrow=False, font=dict(color=SOC_COL, size=12))

# Physical bubble + card
fig.add_shape(type="circle",
              x0=phy_x-oval_w/2, y0=phy_y-oval_h/2, x1=phy_x+oval_w/2, y1=phy_y+oval_h/2,
              fillcolor=PHY_BG, line=dict(color=PHY_OUT, width=2, dash="dash"), layer="below")
fig.add_annotation(x=phy_x, y=phy_y+oval_h/2-0.2, text="<b>Physical dimension</b>",
                   showarrow=False, font=dict(color=PHY_COL, size=12), yshift=10)
fig.add_shape(type="rect",
              x0=phy_x-card_w/2, y0=phy_y-card_h/2, x1=phy_x+card_w/2, y1=phy_y+card_h/2,
              fillcolor="white", line=dict(color=PHY_COL, width=2))
fig.add_annotation(x=phy_x, y=phy_y,
                   text=f"<b>{plus(d_physical)}</b>&nbsp; Physical activity",
                   showarrow=False, font=dict(color=PHY_COL, size=12))

# Environmental bubble + card
fig.add_shape(type="circle",
              x0=env_x-oval_w/2, y0=env_y-oval_h/2, x1=env_x+oval_w/2, y1=env_y+oval_h/2,
              fillcolor=ENV_BG, line=dict(color=ENV_OUT, width=2, dash="dash"), layer="below")
fig.add_annotation(x=env_x, y=env_y+oval_h/2-0.2, text="<b>Environmental dimension</b>",
                   showarrow=False, font=dict(color=ENV_COL, size=12), yshift=10)
fig.add_shape(type="rect",
              x0=env_x-card_w/2, y0=env_y-card_h/2, x1=env_x+card_w/2, y1=env_y+card_h/2,
              fillcolor="white", line=dict(color=ENV_COL, width=2))
fig.add_annotation(x=env_x, y=env_y,
                   text=f"<b>{plus(d_safety)}</b>&nbsp; Safety",
                   showarrow=False, font=dict(color=ENV_COL, size=12))

# QoL box (right)
fig.add_shape(type="rect",
              x0=qol_x-1.8, y0=qol_y-1.6, x1=qol_x+1.8, y1=qol_y+1.6,
              fillcolor=Q_BG, line=dict(color=Q_BR, width=3))
qol_text = (
    f"{plus(q_social)} from Social<br>"
    f"{plus(q_physical)} from Physical<br>"
    f"{plus(q_env)} from Environmental<br>"
    f"<span style='font-size:14px'>——</span><br>"
    f"<b>Δ QoL = {plus(q_total)}</b>"
)
fig.add_annotation(x=qol_x, y=qol_y, text=qol_text, showarrow=False, font=dict(size=12))

# Arrows — Bench → factors (sign-colored)
for (x, y, delta) in [(soc_x, soc_y, d_social), (phy_x, phy_y, d_physical), (env_x, env_y, d_safety)]:
    fig.add_annotation(x=x-1.25, y=y, ax=bench_x+1.4, ay=bench_y,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=2,
                       arrowcolor=sign_color(delta))

# Arrows — factors → QoL
x_q_target = (qol_x - 1.8) + 0.05  # slight nudge so the arrow tip is inside the box

# Top (Social → QoL)
fig.add_annotation(
    x=x_q_target, y=qol_y + 1.2,   # target inside QoL box (above center)
    ax=soc_x + card_w/2, ay=soc_y, # start at Social card
    xref="x", yref="y", axref="x", ayref="y",
    showarrow=True, arrowhead=3, arrowsize=1.1, arrowwidth=3, arrowcolor=GREEN
)

# Middle (Physical → QoL): horizontal
fig.add_annotation(
    x=x_q_target, y=phy_y,
    ax=phy_x + card_w/2, ay=phy_y,
    xref="x", yref="y", axref="x", ayref="y",
    showarrow=True, arrowhead=3, arrowsize=1.1, arrowwidth=3, arrowcolor=GREEN
)

# Bottom (Environmental → QoL)
fig.add_annotation(
    x=x_q_target, y=qol_y - 1.2,   # target inside QoL box (below center)
    ax=env_x + card_w/2, ay=env_y, # start at Environmental card
    xref="x", yref="y", axref="x", ayref="y",
    showarrow=True, arrowhead=3, arrowsize=1.1, arrowwidth=3, arrowcolor=GREEN
)

# Canvas style
fig.update_xaxes(visible=False, range=[0, 10])
fig.update_yaxes(visible=False, range=[0, 10])
fig.update_layout(template="plotly_white", height=540, margin=dict(l=20, r=20, t=20, b=20))

st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------
# Compact KPIs + small QoL gauge
# ------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Δ Social interactions", f"{d_social:+d}")
c2.metric("Δ Physical activity",   f"{d_physical:+d}")
c3.metric("Δ Safety",              f"{d_safety:+d}")
c4.metric("Δ QoL (composite)",     f"{q_total:+d}")

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
    title={"text": "QoL index (mock)"}
))
g.update_layout(height=220, margin=dict(l=10, r=10, t=30, b=10), template="plotly_white")
st.plotly_chart(g, use_container_width=True)

with st.expander("Notes (prototype logic)"):
    st.markdown("""
- Per bench effects (mock): **+2 Social interactions**, **+1 Physical activity**, **−2 Safety**.
- Dimensions contribute to QoL with equal weights (2, 2, 2) → for +1 bench: **+4**, **+2**, **−4**.
- This is a **conceptual** demo to communicate relationships, not a predictive model.
""")
