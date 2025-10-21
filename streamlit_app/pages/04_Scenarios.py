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
    <!-- Perfectly aligned arrowheads -->
    <marker id="arrowGreen1" viewBox="0 0 10 10" refX="10" refY="5"
            markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#19a974"/>
    </marker>
    <marker id="arrowGreen2" viewBox="0 0 12 12" refX="12" refY="6"
            markerWidth="10" markerHeight="10" orient="auto-start-reverse">
      <path d="M 0 0 L 12 6 L 0 12 z" fill="#19a974"/>
    </marker>
    <marker id="arrowRed1" viewBox="0 0 10 10" refX="10" refY="5"
            markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#e85959"/>
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

  <!-- === INTERVENTION BOX === -->
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

  <!-- === DIMENSION BOXES === -->
  <g transform="translate({SOC_X},{SOC_Y})">
    <text x="{DIM_W_SOC/2}" y="10" text-anchor="middle" class="cap" fill="#ff80bf" font-size="16">SOCIAL DIMENSION</text>
    <rect x="0" y="28" rx="{DIM_RX}" ry="{DIM_RX}" width="{DIM_W_SOC}" height="{DIM_H}"
          fill="#fff" stroke="#ff80bf" stroke-width="4" filter="url(#soft)"/>
    <rect x="{PILL_PAD_X}" y="42" rx="{PILL_R}" ry="{PILL_R}"
          width="{DIM_W_SOC - 2*PILL_PAD_X}" height="{PILL_H}" fill="#ff9ad5"/>
    <text x="{DIM_W_SOC/2}" y="68" text-anchor="middle" class="pill">Social networks</text>
  </g>

  <g transform="translate({PHY_X},{PHY_Y})">
    <text x="{DIM_W_PHY/2}" y="10" text-anchor="middle" class="cap" fill="{PHYS_COL}" font-size="16">Physical dimension</text>
    <rect x="0" y="18" rx="{DIM_RX}" ry="{DIM_RX}" width="{DIM_W_PHY}" height="{DIM_H}"
          fill="#fff" stroke="{PHYS_COL}" stroke-width="4" filter="url(#soft)"/>
    <rect x="{PILL_PAD_X}" y="32" rx="{PILL_R}" ry="{PILL_R}"
          width="{DIM_W_PHY - 2*PILL_PAD_X}" height="{PILL_H}" fill="{PHYS_COL}"/>
    <text x="{DIM_W_PHY/2}" y="58" text-anchor="middle" class="pill">Physical activity</text>
  </g>

  <g transform="translate({ENV_X},{ENV_Y})">
    <text x="{DIM_W_ENV/2}" y="10" text-anchor="middle" class="cap" fill="#00b894" font-size="16">ENVIRONMENTAL DIMENSION</text>
    <rect x="0" y="18" rx="{DIM_RX}" ry="{DIM_RX}" width="{DIM_W_ENV}" height="{DIM_H}"
          fill="#fff" stroke="#00b894" stroke-width="4" filter="url(#soft)"/>
    <rect x="{PILL_PAD_X}" y="32" rx="{PILL_R}" ry="{PILL_R}"
          width="{DIM_W_ENV - 2*PILL_PAD_X}" height="{PILL_H}" fill="#00c853"/>
    <text x="{DIM_W_ENV/2}" y="58" text-anchor="middle" class="pill">Safety</text>
  </g>

  <g transform="translate({PSY_X},{PSY_Y})">
    <text x="{DIM_W_PSY/2}" y="10" text-anchor="middle" class="cap" fill="#ff9800" font-size="16">Psychological dimension</text>
    <rect x="0" y="18" rx="{DIM_RX}" ry="{DIM_RX}" width="{DIM_W_PSY}" height="{DIM_H}"
          fill="#fff" stroke="#ff9800" stroke-width="4" filter="url(#soft)"/>
    <rect x="{PILL_PAD_X}" y="32" rx="{PILL_R}" ry="{PILL_R}"
          width="{DIM_W_PSY - 2*PILL_PAD_X}" height="{PILL_H}" fill="#ff8f2d"/>
    <text x="{DIM_W_PSY/2}" y="58" text-anchor="middle" class="pill">Downshift</text>
  </g>

  <!-- === QoL === -->
  <g transform="translate({QOL_X},{QOL_Y})">
    <text x="{Q_W/2}" y="-20" text-anchor="middle" class="cap" fill="#5f9ea0" font-size="18">QUALITY OF LIFE</text>
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

  <!-- === Small numeric bubbles === -->
  <g>
    <g transform="translate({SOC_BADGE_X},{SOC_BADGE_Y})">
      <circle cx="0" cy="0" r="{BADGE_R}" fill="#bdbdbd"/>
      <text x="0" y="4" text-anchor="middle" class="cap" font-size="13" fill="#fff">{sgn(d_social)}</text>
    </g>
    <g transform="translate({PHY_BADGE_X},{PHY_BADGE_Y})">
      <circle cx="0" cy="0" r="{BADGE_R}" fill="#bdbdbd"/>
      <text x="0" y="4" text-anchor="middle" class="cap" font-size="13" fill="#fff">{sgn(d_physical)}</text>
    </g>
    <g transform="translate({ENV_BADGE_X},{ENV_BADGE_Y})">
      <circle cx="0" cy="0" r="{BADGE_R}" fill="#bdbdbd"/>
      <text x="0" y="4" text-anchor="middle" class="cap" font-size="13" fill="#fff">{sgn(d_safety)}</text>
    </g>
    <g transform="translate({PSY_BADGE_X},{PSY_BADGE_Y})">
      <circle cx="0" cy="0" r="{BADGE_R}" fill="#bdbdbd"/>
      <text x="0" y="4" text-anchor="middle" class="cap" font-size="13" fill="#fff">{sgn(d_psych)}</text>
    </g>
  </g>

  <!-- === Arrows + labels (exactly as before) === -->
  <path d="M190,230 C210,170 285,105 339,80" fill="none" stroke="#19a974" stroke-width="{ARROW_W_X2}" marker-end="url(#arrowGreen2)"/>
  <text x="290" y="155" class="cap" font-size="18" fill="#19a974">x2</text>

  <path d="M190,230 C230,220 300,210 370,210" fill="none" stroke="#19a974" stroke-width="{ARROW_W_X1}" marker-end="url(#arrowGreen1)"/>
  <text x="330" y="232" class="cap" font-size="18" fill="#19a974">x1</text>

  <path d="M190,230 C235,275 300,320 355,338" fill="none" stroke="#e85959" stroke-width="{ARROW_W_X1}" marker-end="url(#arrowRed1)"/>
  <text x="295" y="300" class="cap" font-size="18" fill="#e85959">x-1</text>

  <path d="M190,230 C200,320 245,405 344,460" fill="none" stroke="#19a974" stroke-width="{ARROW_W_X1}" marker-end="url(#arrowGreen1)"/>
  <text x="320" y="396" class="cap" font-size="18" fill="#19a974">x1</text>

  <path d="M570,80  C650,95 735,165 768,230" fill="none" stroke="#19a974" stroke-width="{ARROW_W_X2}" marker-end="url(#arrowGreen2)"/>
  <text x="590" y="130" class="cap" font-size="18" fill="#19a974">x2</text>

  <path d="M545,210 C620,210 680,215 773,230" fill="none" stroke="#19a974" stroke-width="{ARROW_W_X1}" marker-end="url(#arrowGreen1)"/>
  <text x="620" y="200" class="cap" font-size="18" fill="#19a974">x1</text>

  <path d="M555,338 C640,320 710,270 768,230" fill="none" stroke="#19a974" stroke-width="{ARROW_W_X2}" marker-end="url(#arrowGreen2)"/>
  <text x="590" y="305" class="cap" font-size="18" fill="#19a974">x2</text>

  <path d="M565,460 C670,440 740,330 768,230" fill="none" stroke="#19a974" stroke-width="{ARROW_W_X1}" marker-end="url(#arrowGreen1)"/>
  <text x="690" y="410" class="cap" font-size="18" fill="#19a974">x1</text>
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
