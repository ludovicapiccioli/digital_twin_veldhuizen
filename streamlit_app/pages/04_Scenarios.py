# pages/04_Scenarios.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Must be first Streamlit call
st.set_page_config(layout="wide", page_title="Scenarios • Veldhuizen")

# Header (keep)
st.subheader("Concept demo - Simulation of scenarios")
st.caption("Concept demo with mock relationships. Adjust benches and see how dimensions and QoL change.")

# ---------------- State & helpers ----------------
BMIN, BMAX = -10, 10
if "b" not in st.session_state:
    st.session_state.b = 0

def clamp(v): return int(max(BMIN, min(BMAX, v)))
def sgn(v):  return f"{int(v):+d}"

# ---------------- Controls (presets + +/- + single slider) ----------------
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("-5 Benches"): st.session_state.b = -5
with c2:
    if st.button("Baseline (0)"): st.session_state.b = 0
with c3:
    if st.button("+5 Benches"): st.session_state.b = +5

cm, cs, cp = st.columns([1, 8, 1])
with cm:
    if st.button("−"): st.session_state.b = clamp(st.session_state.b - 1)
with cp:
    if st.button("＋"): st.session_state.b = clamp(st.session_state.b + 1)
with cs:
    st.slider("Benches (add/remove)", BMIN, BMAX, value=int(st.session_state.b), step=1, key="b")

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

# ---------------- Arrow sizing (weight-aware) ----------------
ARROW_W_X1 = 3.0
ARROW_W_X2 = 4.5
ARROW_W_IN = {
    "social": ARROW_W_X2,
    "physical": ARROW_W_X1,
    "environmental": ARROW_W_X1,
    "psych": ARROW_W_X1,
}

HEAD_W_X1 = 7; HEAD_H_X1 = 7
HEAD_REF_X_X1 = HEAD_W_X1 + 1.0
HEAD_REF_Y_X1 = HEAD_H_X1 / 2

HEAD_W_X2 = 9; HEAD_H_X2 = 9
HEAD_REF_X_X2 = HEAD_W_X2 + 1.0
HEAD_REF_Y_X2 = HEAD_H_X2 / 2

# ---------------- Box sizing (you kept these) ----------------
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

# QoL (unchanged)
Q_W = 160
Q_H = 210
Q_RX = 24
Q_SCORE_H = 96

PHYS_COL = "#B39DDB"  # Physical activity theme color

# ---------------- Positions: center the dimension boxes ----------------
# Canvas is 960px wide. Put the box centers slightly left of center (e.g., 455).
CENTER_X = 455  # tweak this to move all four left/right together

SOC_X = CENTER_X - DIM_W_SOC / 2
PHY_X = CENTER_X - DIM_W_PHY / 2
ENV_X = CENTER_X - DIM_W_ENV / 2
PSY_X = CENTER_X - DIM_W_PSY / 2

SOC_Y = 20
PHY_Y = 160
ENV_Y = 285
PSY_Y = 405

INT_X, INT_Y = 40, 180
QOL_X, QOL_Y = 770, 170

# ---------------- Dynamic SVG ----------------
svg = f'''
<svg viewBox="0 0 960 560" xmlns="http://www.w3.org/2000/svg"
     style="width:100%;height:auto;display:block;background:#ffffff;">

  <defs>
    <!-- Green arrowheads: x1 and x2 -->
    <marker id="arrowGreen1" markerUnits="userSpaceOnUse"
            markerWidth="{HEAD_W_X1}" markerHeight="{HEAD_H_X1}"
            refX="{HEAD_REF_X_X1}" refY="{HEAD_REF_Y_X1}" orient="auto">
      <path d="M0,0 L{HEAD_W_X1},{HEAD_H_X1/2} L0,{HEAD_H_X1} z" fill="#19a974"/>
    </marker>
    <marker id="arrowGreen2" markerUnits="userSpaceOnUse"
            markerWidth="{HEAD_W_X2}" markerHeight="{HEAD_H_X2}"
            refX="{HEAD_REF_X_X2}" refY="{HEAD_REF_Y_X2}" orient="auto">
      <path d="M0,0 L{HEAD_W_X2},{HEAD_H_X2/2} L0,{HEAD_H_X2} z" fill="#19a974"/>
    </marker>

    <!-- Red arrowheads: x1 and x2 -->
    <marker id="arrowRed1" markerUnits="userSpaceOnUse"
            markerWidth="{HEAD_W_X1}" markerHeight="{HEAD_H_X1}"
            refX="{HEAD_REF_X_X1}" refY="{HEAD_REF_Y_X1}" orient="auto">
      <path d="M0,0 L{HEAD_W_X1},{HEAD_H_X1/2} L0,{HEAD_H_X1} z" fill="#e85959"/>
    </marker>
    <marker id="arrowRed2" markerUnits="userSpaceOnUse"
            markerWidth="{HEAD_W_X2}" markerHeight="{HEAD_H_X2}"
            refX="{HEAD_REF_X_X2}" refY="{HEAD_REF_Y_X2}" orient="auto">
      <path d="M0,0 L{HEAD_W_X2},{HEAD_H_X2/2} L0,{HEAD_H_X2} z" fill="#e85959"/>
    </marker>

    <filter id="soft" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.15"/>
    </filter>
    <style>
      .cap {{ font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial; font-weight:600; }}
      .text {{ font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial; }}
      .tiny {{ font-size:12px; fill:#666; }}
      .pill {{ font-size:14px; font-weight:600; fill:#fff; }}
      .score {{ font-size:36px; font-weight:800; fill:#fff; }}
    </style>
  </defs>

  <!-- Left: Intervention -->
  <g transform="translate({INT_X},{INT_Y})">
    <rect x="0" y="0" rx="20" ry="20" width="{INT_W}" height="{INT_H}"
          fill="#fff" stroke="#111" stroke-width="3" filter="url(#soft)"/>
    <text x="{INT_W/2}" y="-18" text-anchor="middle" class="cap" fill="#111" font-size="16">Intervention</text>

    <rect x="{(INT_W-INT_INNER_W)/2}" y="{(INT_H-INT_INNER_H)/2}" rx="20" ry="20"
          width="{INT_INNER_W}" height="{INT_INNER_H}" fill="#000"/>
    <text x="{INT_W/2}" y="{(INT_H/2)+12}" text-anchor="middle" class="pill">Benches</text>

    <g transform="translate(-8,30)">
      <circle cx="20" cy="30" r="20" fill="#bdbdbd"/>
      <text x="20" y="34" text-anchor="middle" class="cap" font-size="15" fill="#fff">{sgn(b)}</text>
    </g>
  </g>

  <!-- Social -->
  <g transform="translate({SOC_X},{SOC_Y})">
    <text x="{DIM_W_SOC/2}" y="18" class="cap" fill="#ff80bf" font-size="16">SOCIAL DIMENSION</text>
    <rect x="0" y="28" rx="{DIM_RX}" ry="{DIM_RX}" width="{DIM_W_SOC}" height="{DIM_H}"
          fill="#ffffff" stroke="#ff80bf" stroke-width="4" filter="url(#soft)"/>
    <rect x="{PILL_PAD_X}" y="42" rx="{PILL_R}" ry="{PILL_R}"
          width="{DIM_W_SOC - 2*PILL_PAD_X}" height="{PILL_H}" fill="#ff9ad5"/>
    <text x="{DIM_W_SOC/2}" y="{42 + PILL_H/2 + 6}" text-anchor="middle" class="pill">Social networks</text>
  </g>

  <!-- Physical -->
  <g transform="translate({PHY_X},{PHY_Y})">
    <text x="{DIM_W_PHY/2}" y="8" class="cap" fill="{PHYS_COL}" font-size="16">Physical dimension</text>
    <rect x="0" y="18" rx="{DIM_RX}" ry="{DIM_RX}" width="{DIM_W_PHY}" height="{DIM_H}"
          fill="#ffffff" stroke="{PHYS_COL}" stroke-width="4" filter="url(#soft)"/>
    <rect x="{PILL_PAD_X}" y="32" rx="{PILL_R}" ry="{PILL_R}"
          width="{DIM_W_PHY - 2*PILL_PAD_X}" height="{PILL_H}" fill="{PHYS_COL}"/>
    <text x="{DIM_W_PHY/2}" y="{32 + PILL_H/2 + 6}" text-anchor="middle" class="pill">Physical activity</text>
  </g>

  <!-- Environmental -->
  <g transform="translate({ENV_X},{ENV_Y})">
    <text x="{DIM_W_ENV/2}" y="8" class="cap" fill="#00b894" font-size="16">ENVIRONMENTAL DIMENSION</text>
    <rect x="0" y="18" rx="{DIM_RX}" ry="{DIM_RX}" width="{DIM_W_ENV}" height="{DIM_H}"
          fill="#ffffff" stroke="#00b894" stroke-width="4" filter="url(#soft)"/>
    <rect x="{PILL_PAD_X}" y="32" rx="{PILL_R}" ry="{PILL_R}"
          width="{DIM_W_ENV - 2*PILL_PAD_X}" height="{PILL_H}" fill="#00c853"/>
    <text x="{DIM_W_ENV/2}" y="{32 + PILL_H/2 + 6}" text-anchor="middle" class="pill">Safety</text>
  </g>

  <!-- Psychological -->
  <g transform="translate({PSY_X},{PSY_Y})">
    <text x="{DIM_W_PSY/2}" y="8" class="cap" fill="#ff9800" font-size="16">Psychological dimension</text>
    <rect x="0" y="18" rx="{DIM_RX}" ry="{DIM_RX}" width="{DIM_W_PSY}" height="{DIM_H}"
          fill="#ffffff" stroke="#ff9800" stroke-width="4" filter="url(#soft)"/>
    <rect x="{PILL_PAD_X}" y="32" rx="{PILL_R}" ry="{PILL_R}"
          width="{DIM_W_PSY - 2*PILL_PAD_X}" height="{PILL_H}" fill="#ff8f2d"/>
    <text x="{DIM_W_PSY/2}" y="{32 + PILL_H/2 + 6}" text-anchor="middle" class="pill">Downshift</text>
  </g>

  <!-- QoL (unchanged position/size) -->
  <g transform="translate({QOL_X},{QOL_Y})">
    <text x="{Q_W/2}" y="-20" class="cap" fill="#5f9ea0" font-size="18">QUALITY OF LIFE</text>
    <rect x="0" y="0" rx="{Q_RX}" ry="{Q_RX}" width="{Q_W}" height="{Q_H}"
          fill="#fff" stroke="#6fa28e" stroke-width="3" filter="url(#soft)"/>
    <g transform="translate(0,{Q_H - Q_SCORE_H})">
      <rect x="0" y="0" rx="{Q_RX}" ry="{Q_RX}" width="{Q_W}" height="{Q_SCORE_H}" fill="#5f8f75"/>
      <text x="{Q_W/2}" y="{Q_SCORE_H*0.65}" text-anchor="middle" class="score">Δ {sgn(q_total)}</text>
    </g>
    <g transform="translate(14,24)">
      <text class="tiny" x="0" y="0">Δ {sgn(q_social)} from Social</text>
      <text class="tiny" x="0" y="18">Δ {sgn(q_physical)} from Physical</text>
      <text class="tiny" x="0" y="36">Δ {sgn(q_env)} from Environmental</text>
      <text class="tiny" x="0" y="54">Δ {sgn(q_psych)} from Psychological</text>
    </g>
  </g>

  <!-- (arrows/badges left as-is; we can parametrize them to auto-follow if you like) -->
</svg>
'''

st.components.v1.html(svg, height=640, scrolling=False)

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
    gauge={
        "axis": {"range": [0, 100]},
        "bar": {"color": "#34495e"},
        "steps": [
            {"range": [0, 40]},
            {"range": [40, 70]},
            {"range": [70, 100]}
        ]
    },
    title={"text": "QoL index (mock)", "font": {"size": 16}}
))
g.update_layout(height=240, margin=dict(l=10, r=10, t=40, b=10), template="plotly_white")
st.plotly_chart(g, use_container_width=True)
