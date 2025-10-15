# pages/04_Scenarios.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Page config FIRST
st.set_page_config(page_title="Scenarios • Veldhuizen", page_icon="🧪", layout="wide")

st.title("🧪 Scenario Sandbox — Benches → Dimensions → QoL")
st.caption("Concept demo (mock relationships). Move the slider and watch the diagram update.")

# ------------------------------------------------------------------
# Slider 
# ------------------------------------------------------------------
b = st.slider("Add / remove benches (Δ units)", -10, 10, 0)

# Per-bench factor effects 
d_social =  2 * b       # +2 per bench
d_physical = 1 * b      # +1 per bench
d_safety = -2 * b       # −2 per bench

# Dimension → QoL weights (+1 bench → +4, +2, −4)
W_SOC, W_PHY, W_ENV = 2, 2, 2
q_social = W_SOC * d_social
q_physical = W_PHY * d_physical
q_env = W_ENV * d_safety
q_total = q_social + q_physical + q_env

# Helpers
def sign_color(v):
    return "#27ae60" if v > 0 else ("#c0392b" if v < 0 else "#7f8c8d")

def plus(v):
    s = f"{int(v):+d}"
    return s if v != 0 else "±0"

# ------------------------------------------------------------------
# Canvas layout (logical coordinates 0..10 x 0..10)
# ------------------------------------------------------------------
# Key positions
bench_x, bench_y = 1.3, 5.0

soc_x,   soc_y   = 4.2, 8.2
phy_x,   phy_y   = 4.2, 5.0
env_x,   env_y   = 4.2, 1.8

qol_x,   qol_y   = 9.0, 5.0

# Bubble sizes
oval_w, oval_h = 3.8, 2.2
card_w, card_h = 2.2, 1.0

# Colors
YELLOW  = "#f1c40f"
SOC_COL = "#e67e22"
SOC_BG  = "#fce9e3"
PHY_COL = "#2980b9"
PHY_BG  = "#e8f1fb"
ENV_COL = "#8e44ad"
ENV_BG  = "#f7e9f5"
Q_BG    = "#b8e994"
Q_BR    = "#78e08f"

# ------------------------------------------------------------------
# Build figure with shapes (boxes, ovals) and annotations (text, arrows)
# ------------------------------------------------------------------
fig = go.Figure()

# BENCH node (left)
fig.add_shape(
    type="rect", x0=bench_x-1.4, y0=bench_y-0.9, x1=bench_x+1.4, y1=bench_y+0.9,
    fillcolor=YELLOW, line=dict(color="#b7950b", width=2), layer="below"
)
fig.add_annotation(x=bench_x, y=bench_y, text=f"<b>{plus(b)} Bench</b>",
                   showarrow=False, font=dict(color="#1f2d3d", size=14))

# SOCIAL cluster (oval) + factor card
fig.add_shape(type="circle",
    x0=soc_x-oval_w/2, y0=soc_y-oval_h/2, x1=soc_x+oval_w/2, y1=soc_y+oval_h/2,
    fillcolor=SOC_BG, line=dict(color="#fadbd8", width=2, dash="dash"), layer="below"
)
fig.add_annotation(x=soc_x, y=soc_y+oval_h/2-0.25, text="<b>Social dimension</b>",
                   showarrow=False, font=dict(color=SOC_COL, size=12), yshift=10)
fig.add_shape(type="rect",
    x0=soc_x-card_w/2, y0=soc_y-card_h/2, x1=soc_x+card_w/2, y1=soc_y+card_h/2,
    fillcolor="white", line=dict(color=SOC_COL, width=2)
)
fig.add_annotation(x=soc_x, y=soc_y, showarrow=False,
                   text=f"<b>{plus(d_social)}</b>&nbsp; Social interactions",
                   font=dict(color=SOC_COL, size=12))

# PHYSICAL cluster (oval) + factor card
fig.add_shape(type="circle",
    x0=phy_x-oval_w/2, y0=phy_y-oval_h/2, x1=phy_x+oval_w/2, y1=phy_y+oval_h/2,
    fillcolor=PHY_BG, line=dict(color="#d6eaf8", width=2, dash="dash"), layer="below"
)
fig.add_annotation(x=phy_x, y=phy_y+oval_h/2-0.25, text="<b>Physical dimension</b>",
                   showarrow=False, font=dict(color=PHY_COL, size=12), yshift=10)
fig.add_shape(type="rect",
    x0=phy_x-card_w/2, y0=phy_y-card_h/2, x1=phy_x+card_w/2, y1=phy_y+card_h/2,
    fillcolor="white", line=dict(color=PHY_COL, width=2)
)
fig.add_annotation(x=phy_x, y=phy_y, showarrow=False,
                   text=f"<b>{plus(d_physical)}</b>&nbsp; Physical activity",
                   font=dict(color=PHY_COL, size=12))

# ENVIRONMENTAL cluster (oval) + factor card
fig.add_shape(type="circle",
    x0=env_x-oval_w/2, y0=env_y-oval_h/2, x1=env_x+oval_w/2, y1=env_y+oval_h/2,
    fillcolor=ENV_BG, line=dict(color="#f5eef8", width=2, dash="dash"), layer="below"
)
fig.add_annotation(x=env_x, y=env_y+oval_h/2-0.25, text="<b>Environmental dimension</b>",
                   showarrow=False, font=dict(color=ENV_COL, size=12), yshift=10)
fig.add_shape(type="rect",
    x0=env_x-card_w/2, y0=env_y-card_h/2, x1=env_x+card_w/2, y1=env_y+card_h/2,
    fillcolor="white", line=dict(color=ENV_COL, width=2)
)
fig.add_annotation(x=env_x, y=env_y, showarrow=False,
                   text=f"<b>{plus(d_safety)}</b>&nbsp; Safety",
                   font=dict(color=ENV_COL, size=12))

# QoL box (right)
fig.add_shape(
    type="rect", x0=qol_x-1.7, y0=qol_y-1.6, x1=qol_x+1.7, y1=qol_y+1.6,
    fillcolor=Q_BG, line=dict(color=Q_BR, width=3)
)
qol_text = (
    f"{plus(q_social)} from Social<br>"
    f"{plus(q_physical)} from Physical<br>"
    f"{plus(q_env)} from Environmental<br>"
    f"<span style='font-size:14px'>——</span><br>"
    f"<b>Δ QoL = {plus(q_total)}</b>"
)
fig.add_annotation(x=qol_x, y=qol_y, text=qol_text, showarrow=False,
                   font=dict(color="#1f2d3d", size=12))

# Arrows Bench → factors (sign-colored)
fig.add_annotation(x=soc_x-1.25, y=soc_y, ax=bench_x+1.4, ay=bench_y,
                   xref="x", yref="y", axref="x", ayref="y",
                   showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=2,
                   arrowcolor=sign_color(d_social))
fig.add_annotation(x=phy_x-1.25, y=phy_y, ax=bench_x+1.4, ay=bench_y,
                   xref="x", yref="y", axref="x", ayref="y",
                   showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=2,
                   arrowcolor=sign_color(d_physical))
fig.add_annotation(x=env_x-1.25, y=env_y, ax=bench_x+1.4, ay=bench_y,
                   xref="x", yref="y", axref="x", ayref="y",
                   showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=2,
                   arrowcolor=sign_color(d_safety))

# Arrows factors → QoL (always green; higher dimension -> higher QoL)
GREEN = "#27ae60"
fig.add_annotation(x=qol_x-1.7, y=soc_y, ax=soc_x+card_w/2, ay=soc_y,
                   xref="x", yref="y", axref="x", ayref="y",
                   showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=2, arrowcolor=GREEN)
fig.add_annotation(x=qol_x-1.7, y=phy_y, ax=phy_x+card_w/2, ay=phy_y,
                   xref="x", yref="y", axref="x", ayref="y",
                   showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=2, arrowcolor=GREEN)
fig.add_annotation(x=qol_x-1.7, y=env_y, ax=env_x+card_w/2, ay=env_y,
                   xref="x", yref="y", axref="x", ayref="y",
                   showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=2, arrowcolor=GREEN)

# Canvas aesthetics
fig.update_xaxes(visible=False, range=[0, 10])
fig.update_yaxes(visible=False, range=[0, 10])
fig.update_layout(
    template="plotly_white",
    height=540,
    margin=dict(l=20, r=20, t=20, b=20),
)

st.plotly_chart(fig, use_container_width=True)

# Small numeric summary under the figure
c1, c2, c3, c4 = st.columns(4)
c1.metric("Δ Social interactions", plus(d_social))
c2.metric("Δ Physical activity", plus(d_physical))
c3.metric("Δ Safety", plus(d_safety))
c4.metric("Δ QoL (composite)", plus(q_total))

with st.expander("Notes (prototype logic)"):
    st.markdown("""
- **Per bench effects**: +2 Social interactions, +1 Physical activity, −2 Safety (mock).
- **Dimension→QoL weights**: Social 2, Physical 2, Environmental 2 ⇒ for +1 bench: **+4**, **+2**, **−4**.
- Diagram is purely illustrative to communicate *cause → dimension → QoL*.
""")
