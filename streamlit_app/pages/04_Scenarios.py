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

# ---------------- Box sizing ----------------
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
CENTER_X = 455  # move this to nudge all dimension boxes L/R together

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

# ---- Precompute anchor points for arrows (so they survive position changes) ----
# Left/right centers of each panel (note: Social panel top padding differs)
SOC_CY = SOC_Y + 28 + DIM_H/2
PHY_CY = PHY_Y + 18 + DIM_H/2
ENV_CY = ENV_Y + 18 + DIM_H/2
PSY_CY = PSY_Y + 18 + DIM_H/2

SOC_LEFT_X  = SOC_X + 8
PHY_LEFT_X  = PHY_X + 8
ENV_LEFT_X  = ENV_X + 8
PSY_LEFT_X  = PSY_X + 8

SOC_RIGHT_X = SOC_X + DIM_W_SOC - 8
PHY_RIGHT_X = PHY_X + DIM_W_PHY - 8
ENV_RIGHT_X = ENV_X + DIM_W_ENV - 8
PSY_RIGHT_X = PSY_X + DIM_W_PSY - 8

# Intervention arrow "hub" (where curves originate)
HUB_X = INT_X + INT_W + 35
HUB_Y = INT_Y + INT_H/2

# QoL left edge points to target (a few vertical positions inside the box)
QOL_LEFT_X = QOL_X + 2
QOL_T_SOCY = QOL_Y + 80
QOL_T_PHYY = QOL_Y + 120
QOL_T_ENVY = QOL_Y + 140
QOL_T_PSYY = QOL_Y + 170

# Curvature knobs (bigger magnitude = more curve)
DX_IN  = 120  # control point distance along x from the hub/card for left-hand arrows
DX_OUT = 120
DY_SOC_UP   = -100
DY_PHY_MID  = 0
DY_ENV_DOWN =  40
DY_PSY_DOWN = 150

DX_DIM2Q   = 130  # x distance for first control point from a dimension to QoL
DX_Q2DIM   = 80   # x distance for second control point before QoL
DY_SOC2Q   = -70
DY_PHY2Q   = -10
DY_ENV2Q   =  10
DY_PSY2Q   =  40

# Build cubic Bezier path strings
def path_in(x0, y0, x1, y1, dy0, dy1):
    """From Intervention hub (x0,y0) to dimension left edge (x1,y1)."""
    c1x, c1y = x0 + DX_IN,  y0 + dy0
    c2x, c2y = x1 - DX_OUT, y1 + dy1
    return f"M{x0:.1f},{y0:.1f} C{c1x:.1f},{c1y:.1f} {c2x:.1f},{c2y:.1f} {x1:.1f},{y1:.1f}"

def path_q(x0, y0, x1, y1, dy0, dy1):
    """From dimension right edge (x0,y0) to QoL left edge (x1,y1)."""
    c1x, c1y = x0 + DX_DIM2Q, y0 + dy0
    c2x, c2y = x1 - DX_Q2DIM, y1 + dy1
    return f"M{x0:.1f},{y0:.1f} C{c1x:.1f},{c1y:.1f} {c2x:.1f},{c2y:.1f} {x1:.1f},{y1:.1f}"

# Left arrows: Intervention -> Dimensions
P_SOC_IN = path_in(HUB_X, HUB_Y, SOC_LEFT_X, SOC_CY, DY_SOC_UP,  -40)
P_PHY_IN = path_in(HUB_X, HUB_Y, PHY_LEFT_X, PHY_CY, DY_PHY_MID,   0)
P_ENV_IN = path_in(HUB_X, HUB_Y, ENV_LEFT_X, ENV_CY,  60,        20)  # red, x-1
P_PSY_IN = path_in(HUB_X, HUB_Y, PSY_LEFT_X, PSY_CY, DY_PSY_DOWN, 40)

# Right arrows: Dimensions -> QoL
P_SOC_Q  = path_q(SOC_RIGHT_X, SOC_CY, QOL_LEFT_X, QOL_T_SOCY, DY_SOC2Q, -40)
P_PHY_Q  = path_q(PHY_RIGHT_X, PHY_CY, QOL_LEFT_X, QOL_T_PHYY, DY_PHY2Q, -10)
P_ENV_Q  = path_q(ENV_RIGHT_X, ENV_CY, QOL_LEFT_X, QOL_T_ENVY, DY_ENV2Q,  10)
P_PSY_Q  = path_q(PSY_RIGHT_X, PSY_CY, QOL_LEFT_X, QOL_T_PSYY, DY_PSY2Q,  30)

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

  <!-- QoL -->
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

  <!-- ===== Arrows: Intervention -> Dimensions (left set) ===== -->
  <path d="{P_SOC_IN}" fill="none" stroke="#19a974"
        stroke-width="{ARROW_W_IN['social']}" marker-end="url(#arrowGreen2)"/>
  <path d="{P_PHY_IN}" fill="none" stroke="#19a974"
        stroke-width="{ARROW_W_IN['physical']}" marker-end="url(#arrowGreen1)"/>
  <path d="{P_ENV_IN}" fill="none" stroke="#e85959"
        stroke-width="{ARROW_W_IN['environmental']}" marker-end="url(#arrowRed1)"/>
  <path d="{P_PSY_IN}" fill="none" stroke="#19a974"
        stroke-width="{ARROW_W_IN['psych']}" marker-end="url(#arrowGreen1)"/>

  <!-- ===== Arrows: Dimensions -> QoL (right set) ===== -->
  <path d="{P_SOC_Q}" fill="none" stroke="#19a974"
        stroke-width="{ARROW_W_X2}" marker-end="url(#arrowGreen2)"/>
  <path d="{P_PHY_Q}" fill="none" stroke="#19a974"
        stroke-width="{ARROW_W_X1}" marker-end="url(#arrowGreen1)"/>
  <path d="{P_ENV_Q}" fill="none" stroke="#19a974"
        stroke-width="{ARROW_W_X2}" marker-end="url(#arrowGreen2)"/>
  <path d="{P_PSY_Q}" fill="none" stroke="#19a974"
        stroke-width="{ARROW_W_X1}" marker-end="url(#arrowGreen1)"/>

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
