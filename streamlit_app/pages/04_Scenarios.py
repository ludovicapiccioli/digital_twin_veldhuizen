# pages/04_Scenarios.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Page config MUST be first Streamlit call in this file
st.set_page_config(page_title="Scenarios • Veldhuizen", layout="wide")

st.subheader("Concept demo - Simulation of scenarios")
st.caption("Concept demo with mock relationships. Adjust benches and see how dimensions and QoL change.")

# ------------------------------------------------------------
# Controls (presets + slider)
# ------------------------------------------------------------
col_p1, col_p2, col_p3 = st.columns(3)
if "bench_delta" not in st.session_state:
    st.session_state.bench_delta = 0

with col_p1:
    if st.button("Baseline (0)"):
        st.session_state.bench_delta = 0
with col_p2:
    if st.button("+5 benches"):
        st.session_state.bench_delta = 5
with col_p3:
    if st.button("-5 benches"):
        st.session_state.bench_delta = -5

b = st.slider("Benches (add/remove)", -10, 10, st.session_state.bench_delta)
st.session_state.bench_delta = b  # keep slider + presets in sync

# ------------------------------------------------------------
# Mock relationships
# ------------------------------------------------------------
# Per-bench effects on factors
d_social   =  2 * b        # +2 per bench
d_physical =  1 * b        # +1 per bench
d_safety   = -2 * b        # −2 per bench (e.g., perceived nuisance)

# Dimension → QoL weights (so +1 bench → +4, +2, −4)
W_SOC, W_PHY, W_ENV = 2, 2, 2
q_social   = W_SOC * d_social
q_physical = W_PHY * d_physical
q_env      = W_ENV * d_safety
q_total    = q_social + q_physical + q_env

def sign_color(v):
    # green for positive, red for negative, grey for zero
    return "#27ae60" if v > 0 else ("#c0392b" if v < 0 else "#7f8c8d")

def plus(v):
    # format with sign
    return f"{int(v):+d}" if isinstance(v, (int, np.integer)) else f"{v:+.0f}"

def stroke_for(v):
    # subtle thickness scale by magnitude (2..6)
    return 2 + min(4, 0.35 * abs(v))

def alpha_for(v):
    # subtle opacity scale by magnitude (0.25..1)
    return 0.25 + min(0.75, 0.075 * abs(v))

# ------------------------------------------------------------
# Diagram as SVG (Drivers-style look)
# ------------------------------------------------------------
# Colors
YELLOW  = "#f1c40f"
SOC_COL = "#e67e22"; SOC_BG = "#fce9e3"; SOC_OUT = "#fadbd8"
PHY_COL = "#2980b9"; PHY_BG = "#e8f1fb"; PHY_OUT = "#d6eaf8"
ENV_COL = "#8e44ad"; ENV_BG = "#f7e9f5"; ENV_OUT = "#f5eef8"
Q_BG    = "#b8e994"; Q_BR   = "#78e08f"
GREEN   = "#27ae60"
DARKTXT = "#1f2d3d"

# Derived visuals for arrows
soc_col  = sign_color(d_social)
phy_col  = sign_color(d_physical)
env_col  = sign_color(d_safety)

soc_sw   = stroke_for(d_social)
phy_sw   = stroke_for(d_physical)
env_sw   = stroke_for(d_safety)

soc_a    = alpha_for(d_social)
phy_a    = alpha_for(d_physical)
env_a    = alpha_for(d_safety)

# Helper to add opacity to hex colors
def with_opacity(hex_color, a):
    # hex -> rgba(r,g,b,a)
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"rgba({r},{g},{b},{a:.3f})"

soc_col_a = with_opacity(soc_col, soc_a)
phy_col_a = with_opacity(phy_col, phy_a)
env_col_a = with_opacity(env_col, env_a)

# Text for cards
bench_label = f"<b>{plus(b)} Bench</b>" if b != 0 else "<b>±0 Bench</b>"
soc_text    = f"<tspan font-weight='700'>{plus(d_social)}</tspan> Social interactions"
phy_text    = f"<tspan font-weight='700'>{plus(d_physical)}</tspan> Physical activity"
env_text    = f"<tspan font-weight='700'>{plus(d_safety)}</tspan> Safety"

# QoL breakdown
qol_lines = [
    f"{plus(q_social)} from Social",
    f"{plus(q_physical)} from Physical",
    f"{plus(q_env)} from Environmental",
]
qol_total = f"{plus(q_total)}"

svg = f"""
<svg id="scenarios-svg" viewBox="0 0 1140 620" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Scenario diagram">
  <defs>
    <!-- Marker arrowheads (scaled with stroke) -->
    <marker id="arrow-green" viewBox="0 0 10 6"
            markerWidth="6.5" markerHeight="6.5"
            refX="8.3" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 z" fill="{GREEN}"/>
    </marker>
    <marker id="arrow-dyn" viewBox="0 0 10 6"
            markerWidth="6.5" markerHeight="6.5"
            refX="8.3" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 z" fill="{DARKTXT}"/>
    </marker>
    <style><![CDATA[
      .title  {{ font: 700 18px 'Inter','Segoe UI',system-ui,-apple-system,sans-serif; fill: {DARKTXT}; }}
      .label  {{ font: 600 14px 'Inter','Segoe UI',system-ui,-apple-system,sans-serif; fill: #fff; }}
      .small  {{ font: 400 13px 'Inter','Segoe UI',system-ui,-apple-system,sans-serif; fill: {DARKTXT}; }}
      .cardt  {{ font: 600 13px 'Inter','Segoe UI',system-ui,-apple-system,sans-serif; fill: {DARKTXT}; }}
      .pill   {{ rx: 22; ry: 22; stroke: #fff; stroke-width: 3; }}
      .oval   {{ stroke-width: 2; stroke-dasharray: 6 6; }}
      .box    {{ rx: 16; ry: 16; }}
    ]]></style>
  </defs>

  <!-- Bench (left) -->
  <rect class="box" x="60" y="240" width="180" height="120"
        fill="{YELLOW}" stroke="#b7950b" stroke-width="3"/>
  <text class="title" x="150" y="270" text-anchor="middle">{bench_label}</text>

  <!-- Social bubble + card -->
  <ellipse class="oval" cx="420" cy="120" rx="110" ry="62"
           fill="{SOC_BG}" stroke="{SOC_OUT}"/>
  <text class="title" x="420" y="60" text-anchor="middle" fill="{SOC_COL}">Social dimension</text>
  <rect class="pill" x="355" y="100" width="130" height="44" fill="#fff" stroke="{SOC_COL}" stroke-width="3"/>
  <text class="cardt" x="420" y="127" text-anchor="middle">{soc_text}</text>

  <!-- Physical bubble + card -->
  <ellipse class="oval" cx="420" cy="300" rx="110" ry="62"
           fill="{PHY_BG}" stroke="{PHY_OUT}"/>
  <text class="title" x="420" y="240" text-anchor="middle" fill="{PHY_COL}">Physical dimension</text>
  <rect class="pill" x="355" y="280" width="130" height="44" fill="#fff" stroke="{PHY_COL}" stroke-width="3"/>
  <text class="cardt" x="420" y="307" text-anchor="middle">{phy_text}</text>

  <!-- Environmental bubble + card -->
  <ellipse class="oval" cx="420" cy="480" rx="110" ry="62"
           fill="{ENV_BG}" stroke="{ENV_OUT}"/>
  <text class="title" x="420" y="420" text-anchor="middle" fill="{ENV_COL}">Environmental dimension</text>
  <rect class="pill" x="355" y="460" width="130" height="44" fill="#fff" stroke="{ENV_COL}" stroke-width="3"/>
  <text class="cardt" x="420" y="487" text-anchor="middle">{env_text}</text>

  <!-- QoL box (right) -->
  <rect class="box" x="860" y="190" width="220" height="240"
        fill="{Q_BG}" stroke="{Q_BR}" stroke-width="3"/>
  <text class="title" x="970" y="215" text-anchor="middle">Quality of Life</text>
  <text class="small" x="970" y="250" text-anchor="middle">{qol_lines[0]}</text>
  <text class="small" x="970" y="270" text-anchor="middle">{qol_lines[1]}</text>
  <text class="small" x="970" y="290" text-anchor="middle">{qol_lines[2]}</text>
  <text class="title" x="970" y="330" text-anchor="middle">Δ QoL = <tspan fill="{DARKTXT}" font-weight="800">{qol_total}</tspan></text>

  <!-- Arrows: Bench -> cards (color by sign, thickness/opacity by |delta|) -->
  <!-- to Social -->
  <path d="M240,300 C300,260 320,170 355,122"
        fill="none" stroke="{soc_col_a}" stroke-width="{soc_sw}" marker-end="url(#arrow-dyn)"/>
  <!-- to Physical -->
  <path d="M240,300 C300,300 320,300 355,302"
        fill="none" stroke="{phy_col_a}" stroke-width="{phy_sw}" marker-end="url(#arrow-dyn)"/>
  <!-- to Environmental -->
  <path d="M240,300 C300,340 320,430 355,478"
        fill="none" stroke="{env_col_a}" stroke-width="{env_sw}" marker-end="url(#arrow-dyn)"/>

  <!-- Arrows: cards -> QoL (always green, gentle curves to different heights) -->
  <!-- Social -> QoL (upper) -->
  <path d="M485,122 C700,90 770,210 860,210"
        fill="none" stroke="{GREEN}" stroke-width="3.5" marker-end="url(#arrow-green)"/>
  <!-- Physical -> QoL (middle) -->
  <path d="M485,302 C700,302 770,290 860,290"
        fill="none" stroke="{GREEN}" stroke-width="3.5" marker-end="url(#arrow-green)"/>
  <!-- Environmental -> QoL (lower) -->
  <path d="M485,482 C700,520 770,370 860,360"
        fill="none" stroke="{GREEN}" stroke-width="3.5" marker-end="url(#arrow-green)"/>
</svg>
"""

st.components.v1.html(svg, height=640, scrolling=False)

# ------------------------------------------------------------
# Compact KPIs + small QoL gauge
# ------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Δ Social interactions", plus(d_social))
c2.metric("Δ Physical activity", plus(d_physical))
c3.metric("Δ Safety", plus(d_safety))
c4.metric("Δ QoL (composite)", plus(q_total))

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
    title={"text": "QoL index (mock)"}
))
g.update_layout(height=220, margin=dict(l=10, r=10, t=30, b=10), template="plotly_white")
st.plotly_chart(g, use_container_width=True)

with st.expander("Notes (prototype logic)"):
    st.markdown("""
- Per bench effects (mock): **+2 Social interactions**, **+1 Physical activity**, **−2 Safety**.
- Dimensions contribute to QoL with equal weights (2, 2, 2) → for +1 bench: **+4**, **+2**, **−4**.
- Arrow **thickness** and **opacity** reflect effect magnitude; arrow **color** reflects sign (green = positive, red = negative, grey = zero).
- This is a **conceptual** demo to communicate relationships, not a predictive model.
""")
