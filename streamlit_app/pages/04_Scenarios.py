# pages/04_Scenarios.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────
# Page config (keep)
# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Scenarios • Veldhuizen", layout="wide")
st.subheader("Concept demo - Simulation of scenarios")
st.caption("Concept demo with mock relationships. Adjust benches and see how dimensions and QoL change.")

# ─────────────────────────────────────────────────────────────
# Styling (for the look of the figures)
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* pill-like preset buttons */
div.stButton > button.pill {
  background: #fff; border: 2px solid #111; color:#111;
  border-radius: 18px; font-weight:700; padding: .35rem 1rem;
}
/* small +/- bump buttons */
div.stButton > button.bump {
  background:#e5e5e5; color:#111; border:0; border-radius:10px;
  font-weight:900; padding:.25rem .65rem;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# State + helpers
# ─────────────────────────────────────────────────────────────
if "bench_delta" not in st.session_state:
    st.session_state.bench_delta = 0

BMIN, BMAX = -10, 10
def clamp(x): return max(BMIN, min(BMAX, int(x)))
def plus(v): return f"{int(v):+d}"
def sign_color(v):  # green, red, grey
    return "#27ae60" if v > 0 else ("#c0392b" if v < 0 else "#7f8c8d")

# ─────────────────────────────────────────────────────────────
# Preset “chips” exactly like the first figure
# ─────────────────────────────────────────────────────────────
pc1, pc2, pc3 = st.columns(3)
with pc1:
    if st.button("-5 Benches", key="p_neg5"): st.session_state.bench_delta = -5
with pc2:
    if st.button("Baseline (0)", key="p_base"): st.session_state.bench_delta = 0
with pc3:
    if st.button("+5 Benches", key="p_pos5"): st.session_state.bench_delta = +5

# add pill class
st.markdown("""
<script>
for (const b of window.parent.document.querySelectorAll('button')) {
  if (['-5 Benches','Baseline (0)','+5 Benches'].includes(b.innerText)) b.classList.add('pill');
}
</script>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Custom control bar (− and ＋, endpoints −10 … +10, current value shown)
# ─────────────────────────────────────────────────────────────
c_minus, c_bar, c_plus = st.columns([0.25, 5, 0.25])
with c_minus:
    if st.button("−", key="dec", use_container_width=True): 
        st.session_state.bench_delta = clamp(st.session_state.bench_delta - 1)
    st.markdown("<script>window.parent.document.querySelectorAll('button')[0]</script>", unsafe_allow_html=True)

with c_plus:
    if st.button("＋", key="inc", use_container_width=True):
        st.session_state.bench_delta = clamp(st.session_state.bench_delta + 1)

b = clamp(st.session_state.bench_delta)
x_pos = (b - BMIN) / (BMAX - BMIN)

fig_bar = go.Figure()
# baseline
fig_bar.add_shape(type="rect", x0=0.05, y0=0.48, x1=0.95, y1=0.52, fillcolor="black", line=dict(width=0))
# end squares
fig_bar.add_shape(type="rect", x0=0.045, y0=0.47, x1=0.055, y1=0.53, fillcolor="black", line=dict(width=0))
fig_bar.add_shape(type="rect", x0=0.945, y0=0.47, x1=0.955, y1=0.53, fillcolor="black", line=dict(width=0))
# knob + current value above
knob_x = 0.05 + 0.90 * x_pos
fig_bar.add_trace(go.Scatter(x=[knob_x], y=[0.5], mode="markers+text",
                             marker=dict(size=16, color="black"),
                             text=[plus(b)], textposition="top center",
                             hoverinfo="skip"))
# labels -10/+10
fig_bar.add_annotation(x=0.05, y=0.35, text=str(BMIN), showarrow=False, font=dict(size=12, color="#555"))
fig_bar.add_annotation(x=0.95, y=0.35, text=f"+{BMAX}", showarrow=False, font=dict(size=12, color="#555"))
fig_bar.update_xaxes(visible=False, range=[0,1]); fig_bar.update_yaxes(visible=False, range=[0,1])
fig_bar.update_layout(template="plotly_white", height=110, margin=dict(l=10, r=10, t=10, b=0))

with c_bar:
    st.plotly_chart(fig_bar, use_container_width=True)

# hidden slider just to allow precise keyboard/mouse control and URL state
b = st.slider("Benches (add/remove)", BMIN, BMAX, value=b, label_visibility="collapsed")
st.session_state.bench_delta = b

# ─────────────────────────────────────────────────────────────
# Model (matches the second figure’s numbers)
# Per bench: +2 social, +1 physical, −1 safety, +1 psychological
# Weights to QoL: Social x2, Physical x1, Environmental x2, Psychological x1
# ─────────────────────────────────────────────────────────────
d_social, d_physical, d_safety, d_psych = 2*b, 1*b, -1*b, 1*b
W_SOC, W_PHY, W_ENV, W_PSY = 2, 1, 2, 1
q_social   = W_SOC * d_social
q_physical = W_PHY * d_physical
q_env      = W_ENV * d_safety
q_psych    = W_PSY * d_psych
q_total    = q_social + q_physical + q_env + q_psych

# ─────────────────────────────────────────────────────────────
# Interactive diagram (layout/colors like the second figure)
# ─────────────────────────────────────────────────────────────
# Node positions (0..10 canvas)
bench_x, bench_y = 1.5, 5.0
soc_x,   soc_y   = 4.2, 8.3
phy_x,   phy_y   = 4.2, 6.0
env_x,   env_y   = 4.2, 3.2
psy_x,   psy_y   = 4.2, 1.0
qol_x,   qol_y   = 9.1, 5.0

oval_w, oval_h = 3.9, 2.2
card_w, card_h = 2.6, 1.05

COL_SOC, COL_PHY, COL_ENV, COL_PSY = "#ff7eb6", "#b50d28", "#138a72", "#f39c12"
QGREEN = "#27ae60"

fig = go.Figure()

# Left black intervention box
fig.add_shape(type="rect", x0=bench_x-1.5, y0=bench_y-1.0, x1=bench_x+1.5, y1=bench_y+1.0,
              fillcolor="black", line=dict(color="#111", width=2), layer="below")
fig.add_shape(type="rect", x0=bench_x-1.6, y0=bench_y-1.1, x1=bench_x+1.6, y1=bench_y+1.1,
              fillcolor="rgba(0,0,0,0)", line=dict(color="#fff", width=2))
fig.add_annotation(x=bench_x, y=bench_y+0.65, text="<b>Intervention</b>", showarrow=False, font=dict(color="#eee", size=12))
fig.add_annotation(x=bench_x, y=bench_y, text="<b>Benches</b>", showarrow=False, font=dict(color="#eee", size=14))
fig.add_annotation(x=bench_x-1.9, y=bench_y+0.9, text=f"<b>{plus(b)}</b>", showarrow=False,
                   font=dict(size=12), bgcolor="#ddd", bordercolor="#bbb", borderwidth=0, xanchor="right")

# helper to draw “bubble + card + grey badge”
def bubble_card(x, y, title, title_color, label, value):
    fig.add_shape(type="circle",  # ellipse via circle bounds
                  x0=x-oval_w/2, y0=y-oval_h/2, x1=x+oval_w/2, y1=y+oval_h/2,
                  fillcolor="rgba(255,255,255,0.6)",
                  line=dict(color="#eee", width=2), layer="below")
    fig.add_annotation(x=x, y=y+oval_h/2-0.2, text=f"<b>{title}</b>", showarrow=False,
                       font=dict(color=title_color, size=13), yshift=10)
    fig.add_shape(type="rect", x0=x-card_w/2, y0=y-card_h/2, x1=x+card_w/2, y1=y+card_h/2,
                  fillcolor="white", line=dict(color=title_color, width=2))
    fig.add_annotation(x=x, y=y, text=f"<b>{label}</b>", showarrow=False,
                       font=dict(color="white", size=12),
                       bgcolor=title_color, bordercolor=title_color)
    fig.add_annotation(x=x+card_w/2+0.35, y=y, text=f"{plus(value)}", showarrow=False,
                       font=dict(size=12), bgcolor="#ddd", bordercolor="#bbb", borderwidth=0)

bubble_card(soc_x, soc_y, "SOCIAL DIMENSION", COL_SOC, "Social networks", d_social)
bubble_card(phy_x, phy_y, "Physical dimension", COL_PHY, "Physical activity", d_physical)
bubble_card(env_x, env_y, "ENVIRONMENTAL DIMENSION", COL_ENV, "Safety", d_safety)
bubble_card(psy_x, psy_y, "Psychological dimension", COL_PSY, "Downshift", d_psych)

# QoL box
fig.add_shape(type="rect", x0=qol_x-2.0, y0=qol_y-1.9, x1=qol_x+2.0, y1=qol_y+1.9,
              fillcolor="#8fb197", line=dict(color="#5e8c6a", width=3))
fig.add_annotation(x=qol_x, y=qol_y+1.1, text="<b>QUALITY OF LIFE</b>", showarrow=False,
                   font=dict(size=14, color="#31563e"))
fig.add_annotation(
    x=qol_x, y=qol_y-0.3,
    text=(f"{plus(q_social)} from Social<br>"
          f"{plus(q_physical)} from Physical<br>"
          f"{plus(q_env)} from Environmental<br>"
          f"{plus(q_psych)} from Psychological"),
    showarrow=False, font=dict(size=12, color="white"),
)
fig.add_annotation(x=qol_x, y=qol_y-1.15, text=f"<b>{int(np.clip(70+q_total,0,100))}</b>",
                   showarrow=False, font=dict(size=26, color="white"))

# arrows
def arrow(x0, y0, x1, y1, color, width):
    fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=3, arrowsize=1.0, arrowwidth=width, arrowcolor=color)

# Intervention → dimensions (sign color)
arrow(bench_x+1.6, bench_y, soc_x-card_w/2, soc_y, sign_color(+1), 4)
arrow(bench_x+1.6, bench_y, phy_x-card_w/2, phy_y, sign_color(+1), 3)
arrow(bench_x+1.6, bench_y, env_x-card_w/2, env_y, sign_color(-1), 3)
arrow(bench_x+1.6, bench_y, psy_x-card_w/2, psy_y, sign_color(+1), 3)

# Dimensions → QoL (green, thickness = weight; with x1/x2 labels)
arrow(soc_x+card_w/2, soc_y, qol_x-2.0+0.05, qol_y+1.25, QGREEN, 5 if W_SOC==2 else 3)
arrow(phy_x+card_w/2, phy_y, qol_x-2.0+0.05, phy_y,       QGREEN, 5 if W_PHY==2 else 3)
arrow(env_x+card_w/2, env_y, qol_x-2.0+0.05, qol_y-1.25, QGREEN, 5 if W_ENV==2 else 3)
arrow(psy_x+card_w/2, psy_y, qol_x-2.0+0.05, qol_y-1.90, QGREEN, 5 if W_PSY==2 else 3)

def weight_label(x, y, w):
    fig.add_annotation(x=x, y=y, text=f"x{w}", showarrow=False,
                       font=dict(size=12, color="#118a52"), bgcolor="white")
weight_label((soc_x+qol_x)/2, qol_y+1.35, W_SOC)
weight_label((phy_x+qol_x)/2, phy_y+0.25, W_PHY)
weight_label((env_x+qol_x)/2, qol_y-1.45, W_ENV)
weight_label((psy_x+qol_x)/2, qol_y-1.85, W_PSY)

fig.update_xaxes(visible=False, range=[0,10]); fig.update_yaxes(visible=False, range=[0,10])
fig.update_layout(template="plotly_white", height=560, margin=dict(l=20, r=20, t=15, b=15))
st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# KPI + Gauge (keep, adapted to new logic; title not cut off)
# ─────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Δ Social interactions", plus(d_social))
c2.metric("Δ Physical activity", plus(d_physical))
c3.metric("Δ Safety", plus(d_safety))
c4.metric("Δ QoL (composite)", plus(q_total))

BASE_QOL = 70
q_after = float(np.clip(BASE_QOL + q_total, 0, 100))
g = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=q_after,
    number={"suffix": " / 100"},
    delta={"reference": BASE_QOL,
           "increasing": {"color": "#27ae60"},
           "decreasing": {"color": "#c0392b"}},
    gauge={"axis": {"range": [0, 100]},
           "bar": {"color": "#34495e"},
           "steps": [{"range": [0, 40]}, {"range": [40, 70]}, {"range": [70, 100]}]},
    title={"text": "QoL index (mock)", "font": {"size": 16}}
))
g.update_layout(height=240, margin=dict(l=10, r=10, t=40, b=10), template="plotly_white")
st.plotly_chart(g, use_container_width=True)

with st.expander("Notes (prototype logic)"):
    st.markdown("""
- Per bench effects (mock): **+2 Social interactions**, **+1 Physical activity**, **−1 Safety**, **+1 Psychological (downshift)**.
- Dimension → QoL weights: **x2** Social, **x1** Physical, **x2** Environmental (safety), **x1** Psychological.
- For +1 bench the QoL components are: **+4 (Social)**, **+1 (Physical)**, **−2 (Environmental)**, **+1 (Psychological)**.
- Conceptual demo only — not a predictive model.
""")
