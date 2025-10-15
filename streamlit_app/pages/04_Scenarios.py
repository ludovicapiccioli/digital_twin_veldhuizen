# pages/04_Scenarios.py
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config 
st.set_page_config(page_title="Scenarios • Veldhuizen", page_icon="🧪", layout="wide")

st.title("🧪 Scenario Sandbox — Benches → QoL")
st.caption("Concept demo with mock relationships. Use the slider and pick the view that feels best for your stakeholders.")

# ------------------------------------------------------------
# Controls
# ------------------------------------------------------------
b = st.slider("Add / remove benches (Δ units)", -10, 10, 0)
view = st.radio("View", ["Diagram (like your sketch)", "Charts (bars + gauge)"], horizontal=True)

# Per-bench factor effects (as in your sketch)
d_social   =  2 * b      # +2 per bench
d_physical =  1 * b      # +1 per bench
d_safety   = -2 * b      # -2 per bench

# Dimension → QoL weights (\+1 bench → +4, +2, −4)
W_SOC, W_PHY, W_ENV = 2, 2, 2
q_social   = W_SOC * d_social
q_physical = W_PHY * d_physical
q_env      = W_ENV * d_safety
q_total    = q_social + q_physical + q_env

# Helpers
def sign_color(v): return "#27ae60" if v > 0 else ("#c0392b" if v < 0 else "#7f8c8d")
def plus(v): return f"{int(v):+d}" if isinstance(v, (int, np.integer)) else f"{v:+.0f}"

# ------------------------------------------------------------
# View 1: Diagram 
# ------------------------------------------------------------
if view.startswith("Diagram"):
    # Canvas positions (0..10)
    bench_x, bench_y = 1.3, 5.0
    soc_x, soc_y = 4.2, 8.2
    phy_x, phy_y = 4.2, 5.0
    env_x, env_y = 4.2, 1.8
    qol_x, qol_y = 9.0, 5.0

    # Bubble/card sizes
    oval_w, oval_h = 3.8, 2.2
    card_w, card_h = 2.2, 1.0

    # Colors
    YELLOW="#f1c40f"; SOC_COL="#e67e22"; SOC_BG="#fce9e3"
    PHY_COL="#2980b9"; PHY_BG="#e8f1fb"; ENV_COL="#8e44ad"; ENV_BG="#f7e9f5"
    Q_BG="#b8e994"; Q_BR="#78e08f"; GREEN="#27ae60"

    fig = go.Figure()

    # Bench box
    fig.add_shape("rect", x0=bench_x-1.4, y0=bench_y-0.9, x1=bench_x+1.4, y1=bench_y+0.9,
                  fillcolor=YELLOW, line=dict(color="#b7950b", width=2), layer="below")
    bench_label = f"<b>{plus(b)} Bench</b>" if b != 0 else "<b>±0 Bench</b>"
    fig.add_annotation(x=bench_x, y=bench_y, text=bench_label, showarrow=False, font=dict(size=14))

    # Social bubble + card
    fig.add_shape("circle", x0=soc_x-oval_w/2, y0=soc_y-oval_h/2, x1=soc_x+oval_w/2, y1=soc_y+oval_h/2,
                  fillcolor=SOC_BG, line=dict(color="#fadbd8", width=2, dash="dash"), layer="below")
    fig.add_annotation(x=soc_x, y=soc_y+oval_h/2-0.2, text="<b>Social dimension</b>",
                       showarrow=False, font=dict(color=SOC_COL, size=12), yshift=10)
    fig.add_shape("rect", x0=soc_x-card_w/2, y0=soc_y-card_h/2, x1=soc_x+card_w/2, y1=soc_y+card_h/2,
                  fillcolor="white", line=dict(color=SOC_COL, width=2))
    fig.add_annotation(x=soc_x, y=soc_y, text=f"<b>{plus(d_social)}</b>&nbsp; Social interactions",
                       showarrow=False, font=dict(color=SOC_COL, size=12))

    # Physical bubble + card
    fig.add_shape("circle", x0=phy_x-oval_w/2, y0=phy_y-oval_h/2, x1=phy_x+oval_w/2, y1=phy_y+oval_h/2,
                  fillcolor=PHY_BG, line=dict(color="#d6eaf8", width=2, dash="dash"), layer="below")
    fig.add_annotation(x=phy_x, y=phy_y+oval_h/2-0.2, text="<b>Physical dimension</b>",
                       showarrow=False, font=dict(color=PHY_COL, size=12), yshift=10)
    fig.add_shape("rect", x0=phy_x-card_w/2, y0=phy_y-card_h/2, x1=phy_x+card_w/2, y1=phy_y+card_h/2,
                  fillcolor="white", line=dict(color=PHY_COL, width=2))
    fig.add_annotation(x=phy_x, y=phy_y, text=f"<b>{plus(d_physical)}</b>&nbsp; Physical activity",
                       showarrow=False, font=dict(color=PHY_COL, size=12))

    # Environmental bubble + card
    fig.add_shape("circle", x0=env_x-oval_w/2, y0=env_y-oval_h/2, x1=env_x+oval_w/2, y1=env_y+oval_h/2,
                  fillcolor=ENV_BG, line=dict(color="#f5eef8", width=2, dash="dash"), layer="below")
    fig.add_annotation(x=env_x, y=env_y+oval_h/2-0.2, text="<b>Environmental dimension</b>",
                       showarrow=False, font=dict(color=ENV_COL, size=12), yshift=10)
    fig.add_shape("rect", x0=env_x-card_w/2, y0=env_y-card_h/2, x1=env_x+card_w/2, y1=env_y+card_h/2,
                  fillcolor="white", line=dict(color=ENV_COL, width=2))
    fig.add_annotation(x=env_x, y=env_y, text=f"<b>{plus(d_safety)}</b>&nbsp; Safety",
                       showarrow=False, font=dict(color=ENV_COL, size=12))

    # QoL box
    fig.add_shape("rect", x0=qol_x-1.8, y0=qol_y-1.6, x1=qol_x+1.8, y1=qol_y+1.6,
                  fillcolor=Q_BG, line=dict(color=Q_BR, width=3))
    qol_text = (
        f"{plus(q_social)} from Social<br>"
        f"{plus(q_physical)} from Physical<br>"
        f"{plus(q_env)} from Environmental<br>"
        f"<span style='font-size:14px'>——</span><br>"
        f"<b>Δ QoL = {plus(q_total)}</b>"
    )
    fig.add_annotation(x=qol_x, y=qol_y, text=qol_text, showarrow=False, font=dict(size=12))

    # Arrows (Bench->factors) sign-colored
    for (x,y,delta) in [(soc_x, soc_y, d_social), (phy_x, phy_y, d_physical), (env_x, env_y, d_safety)]:
        fig.add_annotation(x=x-1.25, y=y, ax=bench_x+1.4, ay=bench_y,
                           xref="x", yref="y", axref="x", ayref="y",
                           showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=2,
                           arrowcolor=sign_color(delta))

    # Arrows (factors->QoL) always green (more of a dimension → higher QoL)
    for (x,y) in [(soc_x, soc_y), (phy_x, phy_y), (env_x, env_y)]:
        fig.add_annotation(x=qol_x-1.8, y=y, ax=x+card_w/2, ay=y,
                           xref="x", yref="y", axref="x", ayref="y",
                           showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=2, arrowcolor="#27ae60")

    fig.update_xaxes(visible=False, range=[0,10]); fig.update_yaxes(visible=False, range=[0,10])
    fig.update_layout(template="plotly_white", height=540, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------
# View 2: Charts (bars + QoL gauge)
# ------------------------------------------------------------
else:
    left, mid, right = st.columns([1.1, 1.2, 1])

    with left:
        st.subheader("Factor changes")
        fac_df = pd.DataFrame({
            "Factor": ["Social interactions", "Physical activity", "Safety"],
            "Δ": [d_social, d_physical, d_safety]
        })
        fac_df["Color"] = fac_df["Δ"].apply(lambda v: "#2ecc71" if v > 0 else ("#e74c3c" if v < 0 else "#95a5a6"))
        fig_fac = px.bar(fac_df, x="Δ", y="Factor", orientation="h",
                         text=fac_df["Δ"].map("{:+d}".format))
        fig_fac.update_traces(marker_color=fac_df["Color"], textposition="outside", cliponaxis=False)
        fig_fac.update_layout(xaxis_title="Change (mock units)", yaxis_title="",
                              template="plotly_white", margin=dict(l=10, r=10, t=20, b=20), height=300)
        st.plotly_chart(fig_fac, use_container_width=True)
        st.metric("Δ QoL (composite)", plus(q_total))

    with mid:
        st.subheader("Contribution to QoL")
        fig_wf = go.Figure(go.Waterfall(
            orientation="v",
            measure=["relative", "relative", "relative", "total"],
            x=["Social", "Physical", "Environmental", "Total"],
            y=[q_social, q_physical, q_env, 0],
            text=[plus(q_social), plus(q_physical), plus(q_env), plus(q_total)],
            textposition="outside",
            increasing={"marker": {"color": "#2ecc71"}},
            decreasing={"marker": {"color": "#e74c3c"}},
            totals={"marker": {"color": "#3498db"}}
        ))
        fig_wf.update_layout(showlegend=False, template="plotly_white",
                             yaxis_title="QoL contribution (mock units)",
                             margin=dict(l=10, r=10, t=20, b=20), height=320)
        st.plotly_chart(fig_wf, use_container_width=True)

    with right:
        st.subheader("Overall QoL (index)")
        BASE_QOL = 70
        qol_after = float(np.clip(BASE_QOL + q_total, 0, 100))
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=qol_after,
            number={"suffix": " / 100"},
            delta={"reference": BASE_QOL,
                   "increasing": {"color": "#2ecc71"},
                   "decreasing": {"color": "#e74c3c"}},
            gauge={"axis": {"range": [0, 100]},
                   "bar": {"color": "#34495e"},
                   "steps": [{"range": [0,40]}, {"range": [40,70]}, {"range": [70,100]}]},
            title={"text": "QoL index (mock)"}
        ))
        fig_g.update_layout(margin=dict(l=10, r=10, t=30, b=10), height=320, template="plotly_white")
        st.plotly_chart(fig_g, use_container_width=True)

# Compact KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Δ Social interactions", plus(d_social))
c2.metric("Δ Physical activity", plus(d_physical))
c3.metric("Δ Safety", plus(d_safety))
c4.metric("Δ QoL (composite)", plus(q_total))

with st.expander("Notes (prototype logic)"):
    st.markdown("""
- Per bench effects (mock): **+2 Social interactions**, **+1 Physical activity**, **−2 Safety**.
- Dimension→QoL weights: Social **2**, Physical **2**, Environmental **2** → for +1 bench: **+4**, **+2**, **−4**.
- This is a concept demo to communicate relationships—not a causal model.
""")
