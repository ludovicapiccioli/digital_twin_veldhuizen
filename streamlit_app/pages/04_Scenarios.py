# pages/04_Scenarios.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ── keep: header ─────────────────────────────────────────────
st.set_page_config(page_title="Scenarios • Veldhuizen", layout="wide")
st.subheader("Concept demo - Simulation of scenarios")
st.caption("Concept demo with mock relationships. Adjust benches and see how dimensions and QoL change.")

# ── state & helpers ─────────────────────────────────────────
BMIN, BMAX = -10, 10
if "benches" not in st.session_state:
    st.session_state.benches = 0

def clamp(v): return int(max(BMIN, min(BMAX, v)))
def plus(v):  return f"{int(v):+d}"
def sign_color(v):  # green / red / grey
    return "#23a455" if v > 0 else ("#d14a3a" if v < 0 else "#7f8c8d")

# ── presets exactly as requested ─────────────────────────────
p1, p2, p3 = st.columns(3)
with p1:
    if st.button("-5 Benches"): st.session_state.benches = -5
with p2:
    if st.button("Baseline (0)"): st.session_state.benches = 0
with p3:
    if st.button("+5 Benches"): st.session_state.benches = +5

# ── single slider with − / ＋ (no duplicates) ───────────────
c_minus, c_slider, c_plus = st.columns([1, 8, 1])
with c_minus:
    if st.button("−"): st.session_state.benches = clamp(st.session_state.benches - 1)
with c_plus:
    if st.button("＋"): st.session_state.benches = clamp(st.session_state.benches + 1)
with c_slider:
    st.slider("Benches (add/remove)", BMIN, BMAX, value=int(st.session_state.benches),
              step=1, key="benches")

b = int(st.session_state.benches)

# ── logic matching the picture ───────────────────────────────
# per bench: +2 Social, +1 Physical, −1 Safety, +1 Psychological
d_social, d_physical, d_safety, d_psych = 2*b, 1*b, -1*b, 1*b
# to QoL weights shown as x2/x1
W_SOC, W_PHY, W_ENV, W_PSY = 2, 1, 2, 1
q_social   = W_SOC * d_social
q_physical = W_PHY * d_physical
q_env      = W_ENV * d_safety
q_psych    = W_PSY * d_psych
q_total    = q_social + q_physical + q_env + q_psych

# ── drawing helpers ──────────────────────────────────────────
def add_arrow(fig, x0, y0, x1, y1, color="#23a455", width=4):
    fig.add_annotation(
        x=x1, y=y1, ax=x0, ay=y0,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=3, arrowsize=1.0,
        arrowwidth=width, arrowcolor=color
    )

def card(fig, *, x, y, title, title_col, label):
    """Colored rectangular card like the screenshot (no ellipses)."""
    # section title above card
    fig.add_annotation(x=x, y=y+0.95, text=f"<b>{title}</b>",
                       showarrow=False, font=dict(size=14, color=title_col))
    # white card with colored border
    fig.add_shape(
        type="rect", x0=x-1.9, y0=y-0.5, x1=x+1.9, y1=y+0.5,
        line=dict(color=title_col, width=3), fillcolor="white"
    )
    # colored inner label
    fig.add_annotation(x=x, y=y, text=f"<b>{label}</b>", showarrow=False,
                       font=dict(size=13, color="white"),
                       bgcolor=title_col, bordercolor=title_col)
    # small grey **square** badge on the right (delta box)
    fig.add_shape(
        type="rect", x0=x+2.2, y0=y-0.22, x1=x+2.52, y1=y+0.22,
        line=dict(color="#bfbfbf", width=1), fillcolor="#d9d9d9"
    )

def badge_text(fig, *, x, y, val):
    fig.add_annotation(x=x, y=y, text=f"{plus(val)}",
                       showarrow=False, font=dict(size=12, color="#444"))

# ── figure ───────────────────────────────────────────────────
# canvas coordinates ~0..10
bench_x, bench_y = 1.2, 5.0
soc_x, soc_y     = 4.7, 8.0
phy_x, phy_y     = 4.7, 5.9
env_x, env_y     = 4.7, 3.7
psy_x, psy_y     = 4.7, 1.6
qol_x, qol_y     = 9.0, 5.0

COL_SOC = "#ff7eb6"  # pink
COL_PHY = "#a20f23"  # deep red
COL_ENV = "#138a72"  # teal-green
COL_PSY = "#f39c12"  # orange
QGREEN  = "#23a455"  # arrows to QoL
QBOX_BG = "#6f8e74"; QBOX_BR = "#4f6f57"

fig = go.Figure()

# left black block
fig.add_shape(type="rect",
              x0=bench_x-3.4, y0=bench_y-1.8, x1=bench_x+0.4, y1=bench_y+1.8,
              fillcolor="black", line=dict(color="black", width=0))
fig.add_annotation(x=bench_x-1.5, y=bench_y+0.7, text="<b>Intervention</b>",
                   showarrow=False, font=dict(color="white", size=14))
fig.add_annotation(x=bench_x-1.5, y=bench_y-0.2, text="<b>Benches</b>",
                   showarrow=False, font=dict(color="white", size=18))

# cards (no ellipses)
card(fig, x=soc_x, y=soc_y, title="SOCIAL DIMENSION", title_col=COL_SOC, label="Social networks")
badge_text(fig, x=soc_x+2.36, y=soc_y, val=d_social)

card(fig, x=phy_x, y=phy_y, title="Physical dimension", title_col=COL_PHY, label="Physical activity")
badge_text(fig, x=phy_x+2.36, y=phy_y, val=d_physical)

card(fig, x=env_x, y=env_y, title="ENVIRONMENTAL DIMENSION", title_col=COL_ENV, label="Safety")
badge_text(fig, x=env_x+2.36, y=env_y, val=d_safety)

card(fig, x=psy_x, y=psy_y, title="Psychological dimension", title_col=COL_PSY, label="Downshift")
badge_text(fig, x=psy_x+2.36, y=psy_y, val=d_psych)

# QoL box
fig.add_shape(type="rect",
              x0=qol_x-2.5, y0=qol_y-2.1, x1=qol_x+2.5, y1=qol_y+2.1,
              fillcolor=QBOX_BG, line=dict(color=QBOX_BR, width=4))
fig.add_annotation(x=qol_x, y=qol_y+1.3, text="<b>QUALITY OF LIFE</b>",
                   showarrow=False, font=dict(size=16, color="#1c3525"))
fig.add_annotation(
    x=qol_x, y=qol_y-0.2, showarrow=False, font=dict(size=12, color="white"),
    text=(f"{plus(q_social)} from Social<br>"
          f"{plus(q_physical)} from Physical<br>"
          f"{plus(q_env)} from Environmental<br>"
          f"{plus(q_psych)} from Psychological")
)
fig.add_annotation(x=qol_x, y=qol_y-1.3,
                   text=f"<b>{int(np.clip(70+q_total,0,100))}</b>",
                   showarrow=False, font=dict(size=32, color="white"))

# arrows: Intervention → dimensions (green/grey/red per sign)
add_arrow(fig, bench_x+0.4, bench_y+0.9, soc_x-2.1, soc_y+0.2, color=sign_color(+1), width=5)
add_arrow(fig, bench_x+0.4, bench_y+0.2, phy_x-2.1, phy_y,     color=sign_color(+1), width=4)
add_arrow(fig, bench_x+0.4, bench_y-0.7, env_x-2.1, env_y,     color=sign_color(-1), width=5)
add_arrow(fig, bench_x+0.4, bench_y-1.4, psy_x-2.1, psy_y-0.1, color=sign_color(+1), width=4)

# arrows: dimensions → QoL (all green; thickness encodes x1/x2)
add_arrow(fig, soc_x+2.1, soc_y+0.1, qol_x-2.5, qol_y+1.1, color=QGREEN, width=7)  # x2
add_arrow(fig, phy_x+2.1, phy_y,     qol_x-2.5, phy_y,       color=QGREEN, width=4)  # x1
add_arrow(fig, env_x+2.1, env_y,     qol_x-2.5, qol_y-1.1,   color=QGREEN, width=7)  # x2
add_arrow(fig, psy_x+2.1, psy_y+0.1, qol_x-2.5, qol_y-2.0,   color=QGREEN, width=4)  # x1

# x1/x2 labels near the green arrows
def wlabel(x, y, w):
    fig.add_annotation(x=x, y=y, text=f"x{w}", showarrow=False,
                       font=dict(size=12, color="#118a52"))
wlabel((soc_x+qol_x)/2, qol_y+1.15, 2)
wlabel((phy_x+qol_x)/2, phy_y+0.18, 1)
wlabel((env_x+qol_x)/2, qol_y-1.15, 2)
wlabel((psy_x+qol_x)/2, qol_y-2.05, 1)

# canvas look
fig.update_xaxes(visible=False, range=[0, 10])
fig.update_yaxes(visible=False, range=[0, 10])
fig.update_layout(template="plotly_white", height=600,
                  margin=dict(l=18, r=18, t=10, b=10))
st.plotly_chart(fig, use_container_width=True)

# ── KPIs + gauge (kept, adapted) ────────────────────────────
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
           "increasing": {"color": "#23a455"},
           "decreasing": {"color": "#d14a3a"}},
    gauge={"axis": {"range": [0, 100]},
           "bar": {"color": "#34495e"},
           "steps": [{"range": [0, 40]}, {"range": [40, 70]}, {"range": [70, 100]}]},
    title={"text": "QoL index (mock)", "font": {"size": 16}}
))
g.update_layout(height=240, margin=dict(l=10, r=10, t=40, b=10), template="plotly_white")
st.plotly_chart(g, use_container_width=True)
