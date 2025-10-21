# pages/04_Scenarios.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────
# Keep: page config + title/caption
# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Scenarios • Veldhuizen", layout="wide")
st.subheader("Concept demo - Simulation of scenarios")
st.caption("Concept demo with mock relationships. Adjust benches and see how dimensions and QoL change.")

# ─────────────────────────────────────────────────────────────
# State & helpers
# ─────────────────────────────────────────────────────────────
BMIN, BMAX = -10, 10
if "benches" not in st.session_state:
    st.session_state.benches = 0

def clamp(v): return int(max(BMIN, min(BMAX, v)))
def plus(v):  return f"{int(v):+d}"
def sign_color(v):  # green / red / grey
    return "#27ae60" if v > 0 else ("#c0392b" if v < 0 else "#7f8c8d")

# ─────────────────────────────────────────────────────────────
# Preset chips (functional, no CSS/JS)
# ─────────────────────────────────────────────────────────────
pc1, pc2, pc3 = st.columns(3)
with pc1:
    if st.button("-5 Benches"): st.session_state.benches = -5
with pc2:
    if st.button("Baseline (0)"): st.session_state.benches = 0
with pc3:
    if st.button("+5 Benches"): st.session_state.benches = +5

# ─────────────────────────────────────────────────────────────
# Single slider with - / + controls (no duplicates)
# ─────────────────────────────────────────────────────────────
c_minus, c_slider, c_plus = st.columns([1, 8, 1])
with c_minus:
    if st.button("−"): st.session_state.benches = clamp(st.session_state.benches - 1)

with c_plus:
    if st.button("＋"): st.session_state.benches = clamp(st.session_state.benches + 1)

with c_slider:
    b = st.slider(
        "Benches (add/remove)", min_value=BMIN, max_value=BMAX,
        step=1, value=int(st.session_state.benches), key="benches"
    )
st.session_state.benches = int(b)

# ─────────────────────────────────────────────────────────────
# Model logic (matches your mock)
# Per bench: +2 Social, +1 Physical, −1 Safety, +1 Psychological
# QoL weights: Social ×2, Physical ×1, Environmental ×2, Psychological ×1
# ─────────────────────────────────────────────────────────────
d_social, d_physical, d_safety, d_psych =  2*b, 1*b, -1*b, 1*b
W_SOC, W_PHY, W_ENV, W_PSY = 2, 1, 2, 1

q_social   = W_SOC * d_social
q_physical = W_PHY * d_physical
q_env      = W_ENV * d_safety
q_psych    = W_PSY * d_psych
q_total    = q_social + q_physical + q_env + q_psych

# ─────────────────────────────────────────────────────────────
# Interactive diagram (shapes, colors, arrows, x1/x2)
# ─────────────────────────────────────────────────────────────
# Canvas (0..10)
bench_x, bench_y = 1.5, 5.0
soc_x, soc_y     = 4.2, 8.3
phy_x, phy_y     = 4.2, 6.0
env_x, env_y     = 4.2, 3.2
psy_x, psy_y     = 4.2, 1.0
qol_x, qol_y     = 9.1, 5.0

oval_w, oval_h = 3.8, 2.2     # ellipse bubble
card_w, card_h = 2.6, 1.05    # white card inside bubble

COL_SOC = "#ff7eb6"   # Social (pink)
COL_PHY = "#b50d28"   # Physical (deep red)
COL_ENV = "#138a72"   # Environmental (teal)
COL_PSY = "#f39c12"   # Psychological (orange)
QGREEN  = "#27ae60"   # QoL arrow green
QBOX_BG = "#8fb197"; QBOX_BR = "#5e8c6a"

fig = go.Figure()

# Left Intervention / Benches block (black with thin white frame)
fig.add_shape("rect", x0=bench_x-1.5, y0=bench_y-1.0, x1=bench_x+1.5, y1=bench_y+1.0,
              fillcolor="black", line=dict(color="#111", width=2), layer="below")
fig.add_shape("rect", x0=bench_x-1.6, y0=bench_y-1.1, x1=bench_x+1.6, y1=bench_y+1.1,
              fillcolor="rgba(0,0,0,0)", line=dict(color="#fff", width=2))
fig.add_annotation(x=bench_x, y=bench_y+0.65, text="<b>Intervention</b>", showarrow=False,
                   font=dict(color="#eee", size=12))
fig.add_annotation(x=bench_x, y=bench_y, text="<b>Benches</b>", showarrow=False,
                   font=dict(color="#eee", size=14))
fig.add_annotation(x=bench_x-1.9, y=bench_y+0.9, text=f"<b>{plus(b)}</b>", showarrow=False,
                   font=dict(size=12), bgcolor="#ddd", bordercolor="#bbb", borderwidth=0, xanchor="right")

# helper: ellipse bubble + white card + small grey badge with delta
def bubble_card(x, y, title, title_color, label, value):
    # ellipse bubble
    fig.add_shape("circle", x0=x-oval_w/2, y0=y-oval_h/2, x1=x+oval_w/2, y1=y+oval_h/2,
                  fillcolor="rgba(255,255,255,0.65)", line=dict(color="#e9e9e9", width=2), layer="below")
    fig.add_annotation(x=x, y=y+oval_h/2-0.2, text=f"<b>{title}</b>", showarrow=False,
                       font=dict(color=title_color, size=13), yshift=10)
    # inner card
    fig.add_shape("rect", x0=x-card_w/2, y0=y-card_h/2, x1=x+card_w/2, y1=y+card_h/2,
                  fillcolor="white", line=dict(color=title_color, width=2))
    fig.add_annotation(x=x, y=y, text=f"<b>{label}</b>", showarrow=False,
                       font=dict(color="white", size=12), bgcolor=title_color, bordercolor=title_color)
    # badge with signed delta
    fig.add_annotation(x=x+card_w/2+0.35, y=y, text=f"{plus(value)}", showarrow=False,
                       font=dict(size=12), bgcolor="#ddd", bordercolor="#bbb", borderwidth=0)

# nodes
bubble_card(soc_x, soc_y, "SOCIAL DIMENSION", COL_SOC, "Social networks", d_social)
bubble_card(phy_x, phy_y, "Physical dimension", COL_PHY, "Physical activity", d_physical)
bubble_card(env_x, env_y, "ENVIRONMENTAL DIMENSION", COL_ENV, "Safety", d_safety)
bubble_card(psy_x, psy_y, "Psychological dimension", COL_PSY, "Downshift", d_psych)

# QoL box
fig.add_shape("rect", x0=qol_x-2.0, y0=qol_y-1.9, x1=qol_x+2.0, y1=qol_y+1.9,
              fillcolor=QBOX_BG, line=dict(color=QBOX_BR, width=3))
fig.add_annotation(x=qol_x, y=qol_y+1.1, text="<b>QUALITY OF LIFE</b>", showarrow=False,
                   font=dict(size=14, color="#31563e"))
fig.add_annotation(x=qol_x, y=qol_y-0.3,
                   text=(f"{plus(q_social)} from Social<br>"
                         f"{plus(q_physical)} from Physical<br>"
                         f"{plus(q_env)} from Environmental<br>"
                         f"{plus(q_psych)} from Psychological"),
                   showarrow=False, font=dict(size=12, color="white"))
fig.add_annotation(x=qol_x, y=qol_y-1.15, text=f"<b>{int(np.clip(70+q_total, 0, 100))}</b>",
                   showarrow=False, font=dict(size=26, color="white"))

# arrow helper
def arrow(x0, y0, x1, y1, color, width):
    fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=3, arrowsize=1.0, arrowwidth=width, arrowcolor=color)

# Intervention → dimensions (sign color)
arrow(bench_x+1.6, bench_y, soc_x-card_w/2, soc_y, sign_color(+1), 4)  # slightly thicker
arrow(bench_x+1.6, bench_y, phy_x-card_w/2, phy_y, sign_color(+1), 3)
arrow(bench_x+1.6, bench_y, env_x-card_w/2, env_y, sign_color(-1), 3)
arrow(bench_x+1.6, bench_y, psy_x-card_w/2, psy_y, sign_color(+1), 3)

# Dimensions → QoL (green; thickness encodes x1/x2 exactly)
arrow(soc_x+card_w/2, soc_y, qol_x-2.0+0.05, qol_y+1.25, QGREEN, 5)  # x2
arrow(phy_x+card_w/2, phy_y, qol_x-2.0+0.05, phy_y,       QGREEN, 3)  # x1
arrow(env_x+card_w/2, env_y, qol_x-2.0+0.05, qol_y-1.25, QGREEN, 5)  # x2
arrow(psy_x+card_w/2, psy_y, qol_x-2.0+0.05, qol_y-1.90, QGREEN, 3)  # x1

# x1/x2 labels near the green arrows
def weight_label(x, y, w):
    fig.add_annotation(x=x, y=y, text=f"x{w}", showarrow=False,
                       font=dict(size=12, color="#118a52"), bgcolor="white")
weight_label((soc_x+qol_x)/2, qol_y+1.35, 2)
weight_label((phy_x+qol_x)/2, phy_y+0.25, 1)
weight_label((env_x+qol_x)/2, qol_y-1.45, 2)
weight_label((psy_x+qol_x)/2, qol_y-1.85, 1)

# canvas
fig.update_xaxes(visible=False, range=[0, 10])
fig.update_yaxes(visible=False, range=[0, 10])
fig.update_layout(template="plotly_white", height=560,
                  margin=dict(l=16, r=16, t=12, b=16))
st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# Keep: KPI + Gauge (adapted; title not cut off)
# ─────────────────────────────────────────────────────────────
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
