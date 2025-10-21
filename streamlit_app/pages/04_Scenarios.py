# pages/04_Scenarios.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ------------------------------------------------------------
# Page config MUST be first Streamlit call in this file
# ------------------------------------------------------------
st.set_page_config(page_title="Scenarios • Veldhuizen", layout="wide")

st.subheader("Concept demo - Simulation of scenarios")
st.caption("Concept demo with mock relationships. Adjust benches and see how dimensions and QoL change.")

# =====================================================================
# SMALL STYLE HELPERS (pure Streamlit-safe CSS)
# =====================================================================
st.markdown("""
<style>
div.stButton > button {
  border-radius: 18px;
  font-weight: 700;
}
div.stButton > button.pill { background:#fff; border:2px solid #111; color:#111; }
div.stButton > button.bump { background:#e6e6e6; color:#111; border:0; border-radius:10px; }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# STATE
# =====================================================================
if "bench_delta" not in st.session_state:
    st.session_state.bench_delta = 0

def clamp(v, a=-10, b=10):
    return max(a, min(b, v))

# =====================================================================
# PRESET BUTTONS (chips like the first figure)
# =====================================================================
p1, p2, p3 = st.columns(3)
with p1:
    if st.button("-5 Benches", key="preset_neg5", use_container_width=True):
        st.session_state.bench_delta = -5
with p2:
    if st.button("Baseline (0)", key="preset_0", use_container_width=True):
        st.session_state.bench_delta = 0
with p3:
    if st.button("+5 Benches", key="preset_pos5", use_container_width=True):
        st.session_state.bench_delta = +5

# make them look like "pills"
st.markdown("""
<script>
for (const b of window.parent.document.querySelectorAll('button')) {
  if (b.innerText === '-5 Benches' || b.innerText === 'Baseline (0)' || b.innerText === '+5 Benches') {
    b.classList.add('pill');
  }
}
</script>
""", unsafe_allow_html=True)

# =====================================================================
# CUSTOM CONTROL BAR (−10 … +10) with − / ＋ and current value
# =====================================================================
BMIN, BMAX = -10, 10
span = BMAX - BMIN

bar_cols = st.columns([0.25, 5, 0.25])
with bar_cols[0]:
    if st.button("−", key="dec", help="Decrease", use_container_width=True):
        st.session_state.bench_delta = clamp(st.session_state.bench_delta - 1)
    st.markdown("<script>window.parent.document.querySelector(\"button[kind='secondary']\");</script>", unsafe_allow_html=True)

with bar_cols[2]:
    if st.button("＋", key="inc", help="Increase", use_container_width=True):
        st.session_state.bench_delta = clamp(st.session_state.bench_delta + 1)

b = int(st.session_state.bench_delta)
x_pos = (b - BMIN) / span

fig_bar = go.Figure()
# baseline line
fig_bar.add_shape(type="rect", x0=0.05, y0=0.48, x1=0.95, y1=0.52,
                  line=dict(color="black", width=0), fillcolor="black")
# end squares
fig_bar.add_shape(type="rect", x0=0.045, y0=0.47, x1=0.055, y1=0.53, fillcolor="black", line=dict(width=0))
fig_bar.add_shape(type="rect", x0=0.945, y0=0.47, x1=0.955, y1=0.53, fillcolor="black", line=dict(width=0))
# knob
knob_x = 0.05 + 0.90 * x_pos
fig_bar.add_trace(go.Scatter(
    x=[knob_x], y=[0.5], mode="markers+text",
    marker=dict(size=16, color="black"),
    text=[f"{b:+d}"], textposition="top center",
    hoverinfo="skip"
))
# labels -10 / +10
fig_bar.add_annotation(x=0.05, y=0.35, text=str(BMIN), showarrow=False, font=dict(size=12, color="#444"))
fig_bar.add_annotation(x=0.95, y=0.35, text=f"+{BMAX}", showarrow=False, font=dict(size=12, color="#444"))

fig_bar.update_xaxes(visible=False, range=[0,1])
fig_bar.update_yaxes(visible=False, range=[0,1])
fig_bar.update_layout(height=110, margin=dict(l=10, r=10, t=10, b=0), template="plotly_white")
with bar_cols[1]:
    st.plotly_chart(fig_bar, use_container_width=True)

# Hidden slider for precise control + state sync
b = st.slider("Benches (add/remove)", BMIN, BMAX, value=b, label_visibility="collapsed", key="slider_sync")
st.session_state.bench_delta = int(b)

# =====================================================================
# MODEL LOGIC (as per figure 2)
# =====================================================================
d_social   =  2 * b   # +2 per bench
d_physical =  1 * b   # +1 per bench
d_safety   = -1 * b   # −1 per bench
d_psych    =  1 * b   # +1 per bench

W_SOC, W_PHY, W_ENV, W_PSY = 2, 1, 2, 1

q_social   = W_SOC * d_social
q_physical = W_PHY * d_physical
q_env      = W_ENV * d_safety
q_psych    = W_PSY * d_psych
q_total    = q_social + q_physical + q_env + q_psych

def sign_color(v):  # green for positive, red for negative, grey for zero
    return "#27ae60" if v > 0 else ("#c0392b" if v < 0 else "#7f8c8d")

def plus(v):
    return f"{int(v):+d}" if isinstance(v, (int, np.integer)) else f"{v:+.0f}"

# =====================================================================
# INTERACTIVE DIAGRAM
# =====================================================================
bench_x, bench_y = 1.5, 5.0
soc_x, soc_y     = 4.2, 8.3
phy_x, phy_y     = 4.2, 5.9
env_x, env_y     = 4.2, 3.2
psy_x, psy_y     = 4.2, 1.0
qol_x, qol_y     = 9.1, 5.0

oval_w, oval_h = 3.9, 2.2
card_w, card_h = 2.5, 1.05

COL_SOC = "#ff7eb6"  # pink label
COL_PHY = "#b50d28"  # deep red label
COL_ENV = "#138a72"  # green label
COL_PSY = "#f39c12"  # orange label

fig = go.Figure()

# Intervention box
fig.add_shape(type="rect",
              x0=bench_x-1.5, y0=bench_y-1.0, x1=bench_x+1.5, y1=bench_y+1.0,
              fillcolor="black", line=dict(color="#111", width=2), layer="below")
fig.add_shape(type="rect",
              x0=bench_x-1.6, y0=bench_y-1.1, x1=bench_x+1.6, y1=bench_y+1.1,
              fillcolor="rgba(0,0,0,0)", line=dict(color="#fff", width=2))
fig.add_annotation(x=bench_x, y=bench_y+0.65, text="<b>Intervention</b>", showarrow=False, font=dict(color="#eee", size=12))
fig.add_annotation(x=bench_x, y=bench_y, text="<b>Benches</b>", showarrow=False, font=dict(color="#eee", size=14))
fig.add_annotation(x=bench_x-1.9, y=bench_y+0.9, text=f"<b>{plus(b)}</b>", showarrow=False,
                   font=dict(size=12), bgcolor="#ddd", bordercolor="#bbb", borderwidth=0, xanchor="right")

# bubble + card + badge — uses ellipse (Plotly circle) instead of rounded-rect
def bubble_card(x, y, title, title_color, card_label, badge_value):
    # ellipse bubble (circle shape with different x/y span)
    fig.add_shape(type="circle",
                  x0=x-oval_w/2, y0=y-oval_h/2, x1=x+oval_w/2, y1=y+oval_h/2,
                  fillcolor="rgba(255,255,255,0.6)",
                  line=dict(color="#eee", width=2), layer="below")
    fig.add_annotation(x=x, y=y+oval_h/2-0.2, text=f"<b>{title}</b>",
                       showarrow=False, font=dict(color=title_color, size=13), yshift=10)
    # card
    fig.add_shape(type="rect",
                  x0=x-card_w/2, y0=y-card_h/2, x1=x+card_w/2, y1=y+card_h/2,
                  fillcolor="white", line=dict(color=title_color, width=2))
    fig.add_annotation(x=x, y=y, text=f"<b>{card_label}</b>", showarrow=False,
                       font=dict(color="white", size=12),
                       bgcolor=title_color, bordercolor=title_color)
    # round badge with delta
    fig.add_annotation(x=x+card_w/2+0.35, y=y, text=f"{plus(badge_value)}",
                       showarrow=False, font=dict(size=12),
                       bgcolor="#ddd", bordercolor="#bbb", borderwidth=0)

# Nodes
bubble_card(soc_x, soc_y, "SOCIAL DIMENSION", COL_SOC, "Social networks", d_social)
bubble_card(phy_x, phy_y, "Physical dimension", COL_PHY, "Physical activity", d_physical)
bubble_card(env_x, env_y, "ENVIRONMENTAL DIMENSION", COL_ENV, "Safety", d_safety)
bubble_card(psy_x, psy_y, "Psychological dimension", COL_PSY, "Downshift", d_psych)

# QoL box
fig.add_shape(type="rect",
              x0=qol_x-2.0, y0=qol_y-1.9, x1=qol_x+2.0, y1=qol_y+1.9,
              fillcolor="#8fb197", line=dict(color="#5e8c6a", width=3))
qol_txt = (
    f"+{q_social} from Social<br>"
    f"{plus(q_physical)} from Physical<br>"
    f"{plus(q_env)} from Environmental<br>"
    f"{plus(q_psych)} from Psychological<br><br>"
    f"<b>{plus(q_total)}</b>"
)
fig.add_annotation(x=qol_x, y=qol_y+1.1, text="<b>QUALITY OF LIFE</b>", showarrow=False,
                   font=dict(size=14, color="#31563e"))
fig.add_annotation(x=qol_x, y=qol_y-0.3, text=qol_txt, showarrow=False, font=dict(size=12, color="white"))
fig.add_annotation(x=qol_x, y=qol_y-1.15, text=f"<b>{int(np.clip(70+q_total,0,100))}</b>",
                   showarrow=False, font=dict(size=26, color="white"))

# Arrow helpers
def arrow(x0, y0, x1, y1, color, width):
    fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=3, arrowsize=1.0, arrowwidth=width, arrowcolor=color)

# Bench → dimensions (color by sign)
arrow(bench_x+1.6, bench_y, soc_x-card_w/2, soc_y, sign_color(+1), 4)
arrow(bench_x+1.6, bench_y, phy_x-card_w/2, phy_y, sign_color(+1), 3)
arrow(bench_x+1.6, bench_y, env_x-card_w/2, env_y, sign_color(-1), 3)
arrow(bench_x+1.6, bench_y, psy_x-card_w/2, psy_y, sign_color(+1), 3)

# dimensions → QoL (thickness = weight)
QGREEN = "#27ae60"
arrow(soc_x+card_w/2, soc_y, qol_x-2.0+0.05, qol_y+1.25, QGREEN, 5 if W_SOC==2 else 3)
arrow(phy_x+card_w/2, phy_y, qol_x-2.0+0.05, phy_y,       QGREEN, 5 if W_PHY==2 else 3)
arrow(env_x+card_w/2, env_y, qol_x-2.0+0.05, qol_y-1.25, QGREEN, 5 if W_ENV==2 else 3)
arrow(psy_x+card_w/2, psy_y, qol_x-2.0+0.05, qol_y-1.9,  QGREEN, 5 if W_PSY==2 else 3)

# Small “x1/x2” labels near green arrows
def weight_label(x, y, w):
    fig.add_annotation(x=x, y=y, text=f"x{w}", showarrow=False,
                       font=dict(size=12, color="#118a52"), bgcolor="white")
weight_label((soc_x+qol_x)/2, qol_y+1.35, W_SOC)
weight_label((phy_x+qol_x)/2, phy_y+0.25, W_PHY)
weight_label((env_x+qol_x)/2, qol_y-1.45, W_ENV)
weight_label((psy_x+qol_x)/2, qol_y-1.85, W_PSY)

fig.update_xaxes(visible=False, range=[0, 10])
fig.update_yaxes(visible=False, range=[0, 10])
fig.update_layout(template="plotly_white", height=560, margin=dict(l=20, r=20, t=15, b=15))
st.plotly_chart(fig, use_container_width=True)

# =====================================================================
# KPIs + QoL gauge (title not clipped)
# =====================================================================
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
