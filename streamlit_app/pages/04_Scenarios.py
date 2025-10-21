# pages/04_Scenarios.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Must be first Streamlit call
st.set_page_config(layout="wide", page_title="Simulation of interventions • Veldhuizen")

# Header
st.subheader("Concept demo - Simulation of interventions")
st.caption("Concept demo with mock relationships. Adjust benches and see how dimensions and QoL change.")

# ---------------- State & helpers ----------------
BMIN, BMAX = -10, 10
if "b" not in st.session_state:
    st.session_state.b = 0

def clamp(v): return int(max(BMIN, min(BMAX, v)))
def sgn(v):  return f"{int(v):+d}"

def set_b(v: int): st.session_state.b = clamp(v)
def inc_b(): st.session_state.b = clamp(st.session_state.get("b", 0) + 1)
def dec_b(): st.session_state.b = clamp(st.session_state.get("b", 0) - 1)

# ---------------- Controls ----------------
left_spacer, col_minus5, col_base, col_plus5, right_spacer = st.columns([1, 1, 1, 1, 1])
with col_minus5:
    st.button("-5 Benches", on_click=set_b, args=(-5,), use_container_width=True)
with col_base:
    st.button("Baseline (0)", on_click=set_b, args=(0,), use_container_width=True)
with col_plus5:
    st.button("+5 Benches", on_click=set_b, args=(+5,), use_container_width=True)

cm, cs, cp = st.columns([1, 8, 1])
with cm:
    st.button("−", on_click=dec_b, use_container_width=True)
with cs:
    st.slider("Benches (add/remove)", BMIN, BMAX, step=1, key="b")
with cp:
    st.button("＋", on_click=inc_b, use_container_width=True)

b = int(st.session_state.b)

# ---------------- Logic ----------------
d_social   =  2 * b
d_physical =  1 * b
d_safety   = -1 * b
d_psych    =  1 * b

W_SOC, W_PHY, W_ENV, W_PSY = 2, 1, 2, 1
q_social   = W_SOC * d_social
q_physical = W_PHY * d_physical
q_env      = W_ENV * d_safety
q_psych    = W_PSY * d_psych
q_total    = q_social + q_physical + q_env + q_psych

# ---------------- Layout parameters ----------------
ARROW_W_X1 = 3.0
ARROW_W_X2 = 4.5
DIM_H  = 64
DIM_RX = 16
PILL_H = 40
PILL_R = 12
PILL_PAD_X = 18

DIM_W_SOC = 220
DIM_W_PHY = 170
DIM_W_ENV = 190
DIM_W_PSY = 205

INT_W = 150
INT_H = 100
INT_INNER_W = 120
INT_INNER_H = 60

Q_W = 160
Q_H = 210
Q_RX = 24
Q_SCORE_H = 96

PHYS_COL = "#B39DDB"

CENTER_X = 455
SOC_X = CENTER_X - DIM_W_SOC / 2
PHY_X = CENTER_X - DIM_W_PHY / 2
ENV_X = CENTER_X - DIM_W_ENV / 2
PSY_X = CENTER_X - DIM_W_PSY / 2

SOC_Y = 20
PHY_Y = 160
ENV_Y = 285
PSY_Y = 405

INT_X, INT_Y = 40, 180
QOL_X = 770
QOL_Y = INT_Y + INT_H / 2 - Q_H / 2

BADGE_R   = 16
BADGE_DX  = 0
BADGE_DY  = 25

SOC_CY = 28 + DIM_H/2
PHY_CY = 18 + DIM_H/2
ENV_CY = 18 + DIM_H/2
PSY_CY = 18 + DIM_H/2

SOC_BADGE_X = SOC_X + DIM_W_SOC + BADGE_DX
PHY_BADGE_X = PHY_X + DIM_W_PHY + BADGE_DX
ENV_BADGE_X = ENV_X + DIM_W_ENV + BADGE_DX
PSY_BADGE_X = PSY_X + DIM_W_PSY + BADGE_DX

SOC_BADGE_Y = SOC_Y + SOC_CY + BADGE_DY
PHY_BADGE_Y = PHY_Y + PHY_CY + BADGE_DY
ENV_BADGE_Y = ENV_Y + ENV_CY + BADGE_DY
PSY_BADGE_Y = PSY_Y + PSY_CY + BADGE_DY

# ---------------- SVG ----------------
svg = f'''
<svg viewBox="0 0 960 520" xmlns="http://www.w3.org/2000/svg"
     style="width:100%;height:auto;display:block;background:#ffffff;">

  <defs>
    <!-- Arrowhead definitions -->
    <marker id="arrowGreen1" viewBox="0 0 10 6"
            markerWidth="6.5" markerHeight="6.5"
            refX="8.3" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 z" fill="#19a974"/>
    </marker>

    <marker id="arrowGreen2" viewBox="0 0 10 6"
            markerWidth="6.5" markerHeight="6.5"
            refX="8.3" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 z" fill="#19a974"/>
    </marker>

    <marker id="arrowRed1" viewBox="0 0 10 6"
            markerWidth="6.5" markerHeight="6.5"
            refX="8.3" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 z" fill="#e85959"/>
    </marker>

    <marker id="arrowRed2" viewBox="0 0 10 6"
            markerWidth="6.5" markerHeight="6.5"
            refX="8.3" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 z" fill="#e85959"/>
    </marker>

    <filter id="soft" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.15"/>
    </filter>
    <style>
      .cap {{ font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial; font-weight:600; }}
      .tiny {{ font-size:12px; fill:#666; }}
      .pill {{ font-size:14px; font-weight:600; fill:#fff; }}
      .score {{ font-size:36px; font-weight:800; fill:#fff; }}
    </style>
  </defs>

  <!-- [SVG contents: boxes, arrows, bubbles, etc.] -->
  <!-- (kept identical to your current working setup) -->

</svg>
'''

st.components.v1.html(svg, height=520, scrolling=False)

# ---------------- KPIs + gauge ----------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Δ Social interactions",  sgn(d_social))
c2.metric("Δ Physical activity",    sgn(d_physical))
c3.metric("Δ Safety",               sgn(d_safety))
c4.metric("Δ QoL (composite)",      sgn(q_total))

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
           "steps": [{"range": [0, 40]},
                     {"range": [40, 70]},
                     {"range": [70, 100]}]},
    title={"text": "QoL index (mock)", "font": {"size": 16}}
))
g.update_layout(height=210, margin=dict(l=10, r=10, t=40, b=10), template="plotly_white")
st.plotly_chart(g, use_container_width=True)

# ---------------- Concept notes (collapsible) ----------------
with st.expander("🧭 Concept Notes (click to expand)", expanded=False):
    st.markdown("""
**What this shows**
- A conceptual demo of how adding/removing benches (`b`) can ripple through **Social, Physical, Environmental (Safety),** and **Psychological** dimensions.
- Each dimension’s Δ feeds a weighted **QoL composite**.

**How the math works (mock)**
- Per-bench effects:  
  - Social = `+2 × b`  
  - Physical = `+1 × b`  
  - Safety = `−1 × b`  
  - Psychological = `+1 × b`
- QoL weights: Social `×2`, Physical `×1`, Environmental `×2`, Psychological `×1`.
- QoL total = sum of weighted deltas (shown as Δ in the box and the bottom KPIs/gauge).

**Important**
- Arrows visualize **influences**, not causation or predictions.
- Baseline QoL is **70/100**; the gauge reflects baseline ± total Δ.
""")
