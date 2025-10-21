# pages/04_Scenarios.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Scenarios • Veldhuizen")

# Keep: title/caption
st.subheader("Concept demo - Simulation of scenarios")
st.caption("Concept demo with mock relationships. Adjust benches and see how dimensions and QoL change.")

# ---------- State & helpers ----------
BMIN, BMAX = -10, 10
if "b" not in st.session_state:
    st.session_state.b = 0

def clamp(v): return int(max(BMIN, min(BMAX, v)))
def sgn(v):  return f"{int(v):+d}"

# ---------- Controls ----------
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

# ---------- Logic ----------
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

# ---------- Dynamic SVG (white background + white dimension panels) ----------
svg = f'''
<svg viewBox="0 0 960 560" xmlns="http://www.w3.org/2000/svg"
     style="width:100%;height:auto;display:block;background:#ffffff;">

  <defs>
    <marker id="arrowGreen" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
      <path d="M0,0 L12,6 L0,12 z" fill="#19a974"/>
    </marker>
    <marker id="arrowRed" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
      <path d="M0,0 L12,6 L0,12 z" fill="#e85959"/>
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
  <g transform="translate(40,180)">
    <rect x="0" y="0" rx="20" ry="20" width="200" height="130" fill="#fff" stroke="#111" stroke-width="3" filter="url(#soft)"/>
    <text x="100" y="-18" text-anchor="middle" class="cap" fill="#111" font-size="16">Intervention</text>
    <rect x="20" y="25" rx="20" ry="20" width="160" height="80" fill="#000"/>
    <text x="100" y="75" text-anchor="middle" class="pill">Benches</text>
    <g transform="translate(-8,35)">
      <circle cx="20" cy="30" r="22" fill="#bdbdbd"/>
      <text x="20" y="35" text-anchor="middle" class="cap" font-size="16" fill="#fff">{sgn(b)}</text>
    </g>
  </g>

  <!-- Social (WHITE background, colored border/label retained) -->
  <g transform="translate(420,20)">
    <text x="160" y="20" class="cap" fill="#ff80bf" font-size="16">SOCIAL DIMENSION</text>
    <rect x="0" y="30" rx="22" ry="22" width="320" height="90" fill="#ffffff" stroke="#ff80bf" stroke-width="4" filter="url(#soft)"/>
    <rect x="30" y="48" rx="18" ry="18" width="260" height="54" fill="#ff9ad5"/>
    <text x="160" y="82" text-anchor="middle" class="pill">Social networks</text>
  </g>

  <!-- Physical -->
  <g transform="translate(420,170)">
    <text x="120" y="10" class="cap" fill="#d90429" font-size="16">Physical dimension</text>
    <rect x="0" y="20" rx="22" ry="22" width="240" height="90" fill="#ffffff" stroke="#d90429" stroke-width="4" filter="url(#soft)"/>
    <rect x="20" y="38" rx="18" ry="18" width="200" height="54" fill="#b60021"/>
    <text x="120" y="72" text-anchor="middle" class="pill">Physical activity</text>
  </g>

  <!-- Environmental -->
  <g transform="translate(420,300)">
    <text x="120" y="10" class="cap" fill="#00b894" font-size="16">ENVIRONMENTAL DIMENSION</text>
    <rect x="0" y="20" rx="22" ry="22" width="260" height="90" fill="#ffffff" stroke="#00b894" stroke-width="4" filter="url(#soft)"/>
    <rect x="30" y="38" rx="18" ry="18" width="200" height="54" fill="#00c853"/>
    <text x="130" y="72" text-anchor="middle" class="pill">Safety</text>
  </g>

  <!-- Psychological -->
  <g transform="translate(420,430)">
    <text x="150" y="10" class="cap" fill="#ff9800" font-size="16">Psychological dimension</text>
    <rect x="0" y="20" rx="22" ry="22" width="300" height="90" fill="#ffffff" stroke="#ff9800" stroke-width="4" filter="url(#soft)"/>
    <rect x="30" y="38" rx="18" ry="18" width="240" height="54" fill="#ff8f2d"/>
    <text x="150" y="72" text-anchor="middle" class="pill">Downshift</text>
  </g>

  <!-- QoL -->
  <g transform="translate(770,170)">
    <text x="100" y="-20" class="cap" fill="#5f9ea0" font-size="18">QUALITY OF LIFE</text>
    <rect x="0" y="0" rx="26" ry="26" width="180" height="230" fill="#fff" stroke="#6fa28e" stroke-width="3" filter="url(#soft)"/>
    <g transform="translate(0,120)">
      <rect x="0" y="0" rx="26" ry="26" width="180" height="110" fill="#5f8f75"/>
      <text x="90" y="70" text-anchor="middle" class="score">{sgn(q_total)}</text>
    </g>
    <g transform="translate(14,24)">
      <text class="tiny" x="0" y="0">{sgn(q_social)} from Social</text>
      <text class="tiny" x="0" y="18">{sgn(q_physical)} from Physical</text>
      <text class="tiny" x="0" y="36">{sgn(q_env)} from Environmental</text>
      <text class="tiny" x="0" y="54">{sgn(q_psych)} from Psychological</text>
    </g>
  </g>

  <!-- Node badges -->
  <g>
    <g transform="translate(740,78)"><circle cx="0" cy="0" r="18" fill="#bdbdbd"/><text x="0" y="5" text-anchor="middle" class="cap" font-size="14" fill="#fff">{sgn(d_social)}</text></g>
    <g transform="translate(670,240)"><circle cx="0" cy="0" r="18" fill="#bdbdbd"/><text x="0" y="5" text-anchor="middle" class="cap" font-size="14" fill="#fff">{sgn(d_physical)}</text></g>
    <g transform="translate(660,372)"><circle cx="0" cy="0" r="18" fill="#bdbdbd"/><text x="0" y="5" text-anchor="middle" class="cap" font-size="14" fill="#fff">{sgn(d_safety)}</text></g>
    <g transform="translate(620,520)"><circle cx="0" cy="0" r="18" fill="#bdbdbd"/><text x="0" y="5" text-anchor="middle" class="cap" font-size="14" fill="#fff">{sgn(d_psych)}</text></g>
  </g>

  <!-- Arrows (unchanged) -->
  <path d="M240,245 C350,140 370,110 440,90"  fill="none" stroke="#19a974" stroke-width="6" marker-end="url(#arrowGreen)"/>
  <text x="335" y="155" class="cap" font-size="18" fill="#19a974">x2</text>

  <path d="M240,245 C330,235 350,230 420,240" fill="none" stroke="#19a974" stroke-width="6" marker-end="url(#arrowGreen)"/>
  <text x="330" y="232" class="cap" font-size="18" fill="#19a974">x1</text>

  <path d="M240,245 C320,300 350,315 420,330" fill="none" stroke="#e85959" stroke-width="6" marker-end="url(#arrowRed)"/>
  <text x="320" y="300" class="cap" font-size="18" fill="#e85959">x-1</text>

  <path d="M240,245 C320,360 360,400 420,460" fill="none" stroke="#19a974" stroke-width="6" marker-end="url(#arrowGreen)"/>
  <text x="320" y="380" class="cap" font-size="18" fill="#19a974">x1</text>

  <path d="M740,90  C800,140 820,220 860,280" fill="none" stroke="#19a974" stroke-width="8" marker-end="url(#arrowGreen)"/>
  <text x="790" y="130" class="cap" font-size="18" fill="#19a974">x2</text>

  <path d="M660,230 C740,230 760,250 860,280" fill="none" stroke="#19a974" stroke-width="6" marker-end="url(#arrowGreen)"/>
  <text x="745" y="225" class="cap" font-size="18" fill="#19a974">x1</text>

  <path d="M680,360 C760,340 780,320 860,300" fill="none" stroke="#19a974" stroke-width="8" marker-end="url(#arrowGreen)"/>
  <text x="755" y="330" class="cap" font-size="18" fill="#19a974">x2</text>

  <path d="M720,480 C780,440 800,420 860,360" fill="none" stroke="#19a974" stroke-width="6" marker-end="url(#arrowGreen)"/>
  <text x="780" y="430" class="cap" font-size="18" fill="#19a974">x1</text>
</svg>
'''

st.components.v1.html(svg, height=640, scrolling=False)

# ---------- KPIs + gauge ----------
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
           "steps": [{"range": [0, 40]}, {"range": [40, 70]}, {"range": [70, 100]}]},
    title={"text": "QoL index (mock)", "font": {"size": 16}}
))
g.update_layout(height=240, margin=dict(l=10, r=10, t=40, b=10), template="plotly_white")
st.plotly_chart(g, use_container_width=True)
