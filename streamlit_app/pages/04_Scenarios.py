# pages/04_Scenarios.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ─────────── Page config + header (keep) ───────────
st.set_page_config(page_title="Scenarios • Veldhuizen", layout="wide")
st.subheader("Concept demo - Simulation of scenarios")
st.caption("Concept demo with mock relationships. Adjust benches and see how dimensions and QoL change.")

# ─────────── State & helpers ───────────
BMIN, BMAX = -10, 10
if "benches" not in st.session_state:
    st.session_state.benches = 0

def clamp(v): return int(max(BMIN, min(BMAX, v)))
def plus(v):  return f"{int(v):+d}"
def sign_color(v):  # green / red / grey
    return "#27ae60" if v > 0 else ("#c0392b" if v < 0 else "#7f8c8d")

# ─────────── Preset chips (exact 3 you requested) ───────────
p1, p2, p3 = st.columns(3)
with p1:
    if st.button("-5 Benches"): st.session_state.benches = -5
with p2:
    if st.button("Baseline (0)"): st.session_state.benches = 0
with p3:
    if st.button("+5 Benches"): st.session_state.benches = +5

# ─────────── Single slider flanked by − / ＋ ───────────
c_minus, c_slider, c_plus = st.columns([1, 8, 1])
with c_minus:
    if st.button("−"): st.session_state.benches = clamp(st.session_state.benches - 1)
with c_plus:
    if st.button("＋"): st.session_state.benches = clamp(st.session_state.benches + 1)
with c_slider:
    st.slider("Benches (add/remove)", BMIN, BMAX, value=int(st.session_state.benches),
              step=1, key="benches")

b = int(st.session_state.benches)

# ─────────── Model logic (exact mapping from your mock) ───────────
# per-bench: Social +2, Physical +1, Environmental(Safety) −1, Psychological +1
d_social, d_physical, d_safety, d_psych = 2*b, 1*b, -1*b, 1*b
# weights to QoL: Social x2, Physical x1, Environmental x2, Psychological x1
W_SOC, W_PHY, W_ENV, W_PSY = 2, 1, 2, 1
q_social   = W_SOC * d_social
q_physical = W_PHY * d_physical
q_env      = W_ENV * d_safety
q_psych    = W_PSY * d_psych
q_total    = q_social + q_physical + q_env + q_psych

# ─────────── Interactive diagram (layout to match your figure) ───────────
# canvas coordinates ~0..10
bench_x, bench_y = 1.3, 5.0
soc_x, soc_y     = 4.1, 8.25
phy_x, phy_y     = 4.1, 6.05
env_x, env_y     = 4.1, 3.4
psy_x, psy_y     = 4.1, 1.1
qol_x, qol_y     = 9.0, 5.0

# sizes
oval_w, oval_h = 4.2, 2.3     # grey ellipse background
card_w, card_h = 3.3, 1.2     # inner white card

# colors (close to your mock)
COL_SOC = "#ff7eb6"  # pink
COL_PHY = "#a20f23"  # deep red
COL_ENV = "#138a72"  # teal green
COL_PSY = "#f39c12"  # orange
QGREEN  = "#23a455"
QBOX_BG = "#6f8e74"; QBOX_BR = "#4f6f57"

fig = go.Figure()

# Left black intervention box
fig.add_shape(type="rect", x0=bench_x-2.7, y0=bench_y-1.6, x1=bench_x+0.7, y1=bench_y+1.6,
              fillcolor="black", line=dict(color="black", width=0))
fig.add_annotation(x=bench_x-1.0, y=bench_y+0.6, text="<b>Intervention</b>",
                   showarrow=False, font=dict(color="white", size=14))
fig.add_annotation(x=bench_x-1.0, y=bench_y-0.2, text="<b>Benches</b>",
                   showarrow=False, font=dict(color="white", size=18))

# helper: grey ellipse + colored card + tiny grey delta badge
def node(x, y, title, title_color, label, value):
    # light grey ellipse background
    fig.add_shape(type="circle", x0=x-oval_w/2, y0=y-oval_h/2, x1=x+oval_w/2, y1=y+oval_h/2,
                  fillcolor="rgba(0,0,0,0)", line=dict(color="#e5e5e5", width=3), layer="below")
    fig.add_annotation(x=x, y=y+oval_h/2-0.25, text=f"<b>{title}</b>", showarrow=False,
                       font=dict(color=title_color, size=14))
    # inner white card with colored border
    fig.add_shape(type="rect", x0=x-card_w/2, y0=y-card_h/2, x1=x+card_w/2, y1=y+card_h/2,
                  fillcolor="white", line=dict(color=title_color, width=3))
    fig.add_annotation(x=x, y=y, text=f"<b>{label}</b>", showarrow=False,
                       font=dict(color="white", size=13),
                       bgcolor=title_color, bordercolor=title_color)
    # small grey rounded badge to the right with signed delta
    fig.add_shape(type="circle", x0=x+card_w/2+0.25-0.20, y0=y-0.20, x1=x+card_w/2+0.25+0.20, y1=y+0.20,
                  fillcolor="#d9d9d9", line=dict(color="#bfbfbf", width=1))
    fig.add_annotation(x=x+card_w/2+0.25, y=y, text=f"{plus(value)}",
                       showarrow=False, font=dict(size=12, color="#444"))

# nodes in order
node(soc_x, soc_y, "SOCIAL DIMENSION", COL_SOC, "Social networks", d_social)
node(phy_x, phy_y, "Physical dimension", COL_PHY, "Physical activity", d_physical)
node(env_x, env_y, "ENVIRONMENTAL DIMENSION", COL_ENV, "Safety", d_safety)
node(psy_x, psy_y, "Psychological dimension", COL_PSY, "Downshift", d_psych)

# QoL box on the right
fig.add_shape(type="rect", x0=qol_x-2.3, y0=qol_y-2.0, x1=qol_x+2.3, y1=qol_y+2.0,
              fillcolor=QBOX_BG, line=dict(color=QBOX_BR, width=4))
fig.add_annotation(x=qol_x, y=qol_y+1.2, text="<b>QUALITY OF LIFE</b>", showarrow=False,
                   font=dict(size=16, color="#1c3525"))
fig.add_annotation(
    x=qol_x, y=qol_y-0.3, showarrow=False, font=dict(size=12, color="white"),
    text=(f"{plus(0 if q_social==0 else q_social)} from Social<br>"
          f"{plus(0 if q_physical==0 else q_physical)} from Physical<br>"
          f"{plus(0 if q_env==0 else q_env)} from Environmental<br>"
          f"{plus(0 if q_psych==0 else q_psych)} from Psychological")
)
fig.add_annotation(x=qol_x, y=qol_y-1.2,
                   text=f"<b>{int(np.clip(70+q_total,0,100))}</b>",
                   showarrow=False, font=dict(size=32, color="white"))

# Arrows helper
def arrow(x0, y0, x1, y1, color, width):
    fig.add_annotation(
        x=x1, y=y1, ax=x0, ay=y0,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=3, arrowsize=1.0,
        arrowwidth=width, arrowcolor=color
    )

# Intervention → dimensions (color by sign; thin like mock)
arrow(bench_x+0.7, bench_y, soc_x-card_w/2-0.2, soc_y+0.1, sign_color(+1), 3)
arrow(bench_x+0.7, bench_y, phy_x-card_w/2-0.2, phy_y-0.1, sign_color(+1), 3)
arrow(bench_x+0.7, bench_y-0.2, env_x-card_w/2-0.2, env_y+0.1, sign_color(-1), 3)
arrow(bench_x+0.7, bench_y-0.9, psy_x-card_w/2-0.2, psy_y, sign_color(+1), 3)

# Dimensions → QoL (all green; thickness encodes x1/x2, labels “x1”, “x2”)
arrow(soc_x+card_w/2+0.2, soc_y, qol_x-2.3, qol_y+1.1, QGREEN, 7)  # x2 (thicker)
arrow(phy_x+card_w/2+0.2, phy_y, qol_x-2.3, phy_y,       QGREEN, 4)  # x1
arrow(env_x+card_w/2+0.2, env_y, qol_x-2.3, qol_y-1.1, QGREEN, 7)   # x2
arrow(psy_x+card_w/2+0.2, psy_y, qol_x-2.3, qol_y-2.0, QGREEN, 4)   # x1

# x1/x2 text near the green arrows (exact positions)
def wlabel(x, y, w): fig.add_annotation(x=x, y=y, text=f"x{w}", showarrow=False,
                                        font=dict(size=12, color="#118a52"))
wlabel((soc_x+qol_x)/2, qol_y+1.15, 2)
wlabel((phy_x+qol_x)/2, phy_y+0.18, 1)
wlabel((env_x+qol_x)/2, qol_y-1.15, 2)
wlabel((psy_x+qol_x)/2, qol_y-2.05, 1)

# canvas look
fig.update_xaxes(visible=False, range=[0, 10])
fig.update_yaxes(visible=False, range=[0, 10])
fig.update_layout(template="plotly_white", height=580,
                  margin=dict(l=20, r=20, t=12, b=12))
st.plotly_chart(fig, use_container_width=True)

# ─────────── KPI + Gauge (kept; adapted to new logic) ───────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Δ Social interactions", plus(d_social))
c2.metric("Δ Physical activity",   plus(d_physical))
c3.metric("Δ Safety",              plus(d_safety))
c4.metric("Δ QoL (composite)",     plus(q_total))

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
