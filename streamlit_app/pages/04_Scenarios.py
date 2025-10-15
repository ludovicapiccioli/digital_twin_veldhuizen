# pages/04_Scenarios.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Scenarios • Veldhuizen", page_icon="🧪", layout="wide")

st.title("🧪 Scenario Sandbox — Benches → Dimensions → QoL")
st.caption("Concept demo (mock relationships). Move the slider and watch the diagram update.")

# Slider
b = st.slider("Add / remove benches (Δ units)", -10, 10, 0)

# Per-bench effects
d_social   =  2 * b
d_physical =  1 * b
d_safety   = -2 * b

# Dimension → QoL weights (so +1 bench → +4, +2, −4)
W_SOC, W_PHY, W_ENV = 2, 2, 2
q_social   = W_SOC * d_social
q_physical = W_PHY * d_physical
q_env      = W_ENV * d_safety
q_total    = q_social + q_physical + q_env

def sign_color(v): return "#27ae60" if v > 0 else ("#c0392b" if v < 0 else "#7f8c8d")
def plus(v): return f"{int(v):+d}" if isinstance(v, (int, np.integer)) else f"{v:+.0f}"

# Layout coords
bench_x, bench_y = 1.3, 5.0
soc_x, soc_y     = 4.2, 8.2
phy_x, phy_y     = 4.2, 5.0
env_x, env_y     = 4.2, 1.8
qol_x, qol_y     = 9.0, 5.0

oval_w, oval_h = 3.8, 2.2
card_w, card_h = 2.2, 1.0

# Colors
YELLOW="#f1c40f"; SOC_COL="#e67e22"; SOC_BG="#fce9e3"
PHY_COL="#2980b9"; PHY_BG="#e8f1fb"; ENV_COL="#8e44ad"; ENV_BG="#f7e9f5"
Q_BG="#b8e994"; Q_BR="#78e08f"; GREEN="#27ae60"

fig = go.Figure()

# Bench
fig.add_shape(type="rect", x0=bench_x-1.4, y0=bench_y-0.9, x1=bench_x+1.4, y1=bench_y+0.9,
              fillcolor=YELLOW, line=dict(color="#b7950b", width=2), layer="below")
bench_label = f"<b>{plus(b)} Bench</b>" if b != 0 else "<b>±0 Bench</b>"
fig.add_annotation(x=bench_x, y=bench_y, text=bench_label, showarrow=False, font=dict(size=14))

# Social bubble + card
fig.add_shape(type="circle", x0=soc_x-oval_w/2, y0=soc_y-oval_h/2, x1=soc_x+oval_w/2, y1=soc_y+oval_h/2,
              fillcolor=SOC_BG, line=dict(color="#fadbd8", width=2, dash="dash"), layer="below")
fig.add_annotation(x=soc_x, y=soc_y+oval_h/2-0.2, text="<b>Social dimension</b>",
                   showarrow=False, font=dict(color=SOC_COL, size=12), yshift=10)
fig.add_shape(type="rect", x0=soc_x-card_w/2, y0=soc_y-card_h/2, x1=soc_x+card_w/2, y1=soc_y+card_h/2,
              fillcolor="white", line=dict(color=SOC_COL, width=2))
fig.add_annotation(x=soc_x, y=soc_y, text=f"<b>{plus(d_social)}</b>&nbsp; Social interactions",
                   showarrow=False, font=dict(color=SOC_COL, size=12))

# Physical bubble + card
fig.add_shape(type="circle", x0=phy_x-oval_w/2, y0=phy_y-oval_h/2, x1=phy_x+oval_w/2, y1=phy_y+oval_h/2,
              fillcolor=PHY_BG, line=dict(color="#d6eaf8", width=2, dash="dash"), layer="below")
fig.add_annotation(x=phy_x, y=phy_y+oval_h/2-0.2, text="<b>Physical dimension</b>",
                   showarrow=False, font=dict(color=PHY_COL, size=12), yshift=10)
fig.add_shape(type="rect", x0=phy_x-card_w/2, y0=phy_y-card_h/2, x1=phy_x+card_w/2, y1=phy_y+card_h/2,
              fillcolor="white", line=dict(color=PHY_COL, width=2))
fig.add_annotation(x=phy_x, y=phy_y, text=f"<b>{plus(d_physical)}</b>&nbsp; Physical activity",
                   showarrow=False, font=dict(color=PHY_COL, size=12))

# Environmental bubble + card
fig.add_shape(type="circle", x0=env_x-oval_w/2, y0=env_y-oval_h/2, x1=env_x+oval_w/2, y1=env_y+oval_h/2,
              fillcolor=ENV_BG, line=dict(color="#f5eef8", width=2, dash="dash"), layer="below")
fig.add_annotation(x=env_x, y=env_y+oval_h/2-0.2, text="<b>Environmental dimension</b>",
                   showarrow=False, font=dict(color=ENV_COL, size=12), yshift=10)
fig.add_shape(type="rect", x0=env_x-card_w/2, y0=env_y-card_h/2, x1=env_x+card_w/2, y1=env_y+card_h/2,
              fillcolor="white", line=dict(color=ENV_COL, width=2))
fig.add_annotation(x=env_x, y=env_y, text=f"<b>{plus(d_safety)}</b>&nbsp; Safety",
                   showarrow=False, font=dict(color=ENV_COL, size=12))

# QoL box
fig.add_shape(type="rect", x0=qol_x-1.8, y0=qol_y-1.6, x1=qol_x+1.8, y1=qol_y+1.6,
              fillcolor=Q_BG, line=dict(color=Q_BR, width=3))
qol_text = (
    f"{plus(q_social)} from Social<br>"
    f"{plus(q_physical)} from Physical<br>"
    f"{plus(q_env)} from Environmental<br>"
    f"<span style='font-size:14px'>——</span><br>"
    f"<b>Δ QoL = {plus(q_total)}</b>"
)
fig.add_annotation(x=qol_x, y=qol_y, text=qol_text, showarrow=False, font=dict(size=12))

# Arrows Bench → factors (sign-colored)
for (x, y, delta) in [(soc_x, soc_y, d_social), (phy_x, phy_y, d_physical), (env_x, env_y, d_safety)]:
    fig.add_annotation(x=x-1.25, y=y, ax=bench_x+1.4, ay=bench_y,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=2,
                       arrowcolor=sign_color(delta))

# Arrows factors → QoL (always green)
for (x, y) in [(soc_x, soc_y), (phy_x, phy_y), (env_x, env_y)]:
    fig.add_annotation(x=qol_x-1.8, y=y, ax=x+card_w/2, ay=y,
                       xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=2,
                       arrowcolor=GREEN)

# Canvas
fig.update_xaxes(visible=False, range=[0, 10])
fig.update_yaxes(visible=False, range=[0, 10])
fig.update_layout(template="plotly_white", height=540, margin=dict(l=20, r=20, t=20, b=20))

st.plotly_chart(fig, use_container_width=True)

# KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Δ Social interactions", plus(d_social))
c2.metric("Δ Physical activity", plus(d_physical))
c3.metric("Δ Safety", plus(d_safety))
c4.metric("Δ QoL (composite)", plus(q_total))

with st.expander("Notes (prototype logic)"):
    st.markdown("""
- Per bench effects (mock): **+2 Social interactions**, **+1 Physical activity**, **−2 Safety**.
- Dimension→QoL weights: Social **2**, Physical **2**, Environmental **2** → for +1 bench: **+4**, **+2**, **−4**.
- Diagram is illustrative to communicate *cause → dimension → QoL* (not predictive).
""")
