# pages/04_Scenarios.py
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config 
st.set_page_config(page_title="Scenarios • Veldhuizen", page_icon="🧪", layout="wide")

st.title("Scenarios — Visual Demo")
st.caption("Adjust benches and see factor changes, QoL contributions, and an overall QoL gauge. (Conceptual mock, not predictive.)")

# ---------------------------
# Controls
# ---------------------------
b = st.slider("Add / remove benches (Δ units)", -10, 10, 0)

# Per-bench factor effects (from your sketch)
d_social =  2 * b        # +2 per bench
d_physical = 1 * b       # +1 per bench
d_safety = -2 * b        # −2 per bench (e.g., perceived nuisance)

# Dimension→QoL weights tuned to show +4, +2, −4 for +1 bench
W_SOC, W_PHY, W_ENV = 2, 2, 2
qol_social = W_SOC * d_social
qol_physical = W_PHY * d_physical
qol_env = W_ENV * d_safety
qol_delta = qol_social + qol_physical + qol_env

# Optional baseline QoL just for the gauge
BASE_QOL = 70
qol_after = float(np.clip(BASE_QOL + qol_delta, 0, 100))

# ---------------------------
# Layout
# ---------------------------
left, mid, right = st.columns([1.1, 1.2, 1])

# 1) Factor change bars (green/red)
with left:
    st.subheader("Factor changes")
    fac_df = pd.DataFrame({
        "Factor": ["Social interactions", "Physical activity", "Safety"],
        "Δ": [d_social, d_physical, d_safety]
    })
    fac_df["Color"] = fac_df["Δ"].apply(lambda v: "#2ecc71" if v > 0 else ("#e74c3c" if v < 0 else "#95a5a6"))
    fig_fac = px.bar(
        fac_df, x="Δ", y="Factor", orientation="h",
        text=fac_df["Δ"].map("{:+d}".format),
    )
    fig_fac.update_traces(marker_color=fac_df["Color"], textposition="outside", cliponaxis=False)
    fig_fac.update_layout(
        xaxis_title="Change (mock units)", yaxis_title="", template="plotly_white",
        margin=dict(l=10, r=10, t=20, b=20), height=300
    )
    st.plotly_chart(fig_fac, use_container_width=True)
    st.metric("Δ QoL (composite)", f"{qol_delta:+.0f}")

# 2) QoL contribution waterfall
with mid:
    st.subheader("Contribution to QoL")
    fig_wf = go.Figure(go.Waterfall(
        orientation="v",
        measure=["relative", "relative", "relative", "total"],
        x=["Social", "Physical", "Environmental", "Total"],
        y=[qol_social, qol_physical, qol_env, 0],
        text=[f"{qol_social:+.0f}", f"{qol_physical:+.0f}", f"{qol_env:+.0f}", f"{qol_delta:+.0f}"],
        textposition="outside",
        increasing={"marker": {"color": "#2ecc71"}},
        decreasing={"marker": {"color": "#e74c3c"}},
        totals={"marker": {"color": "#3498db"}}
    ))
    fig_wf.update_layout(
        showlegend=False, template="plotly_white",
        yaxis_title="QoL contribution (mock units)",
        margin=dict(l=10, r=10, t=20, b=20), height=320
    )
    st.plotly_chart(fig_wf, use_container_width=True)

# 3) QoL gauge (before vs after)
with right:
    st.subheader("Overall QoL (index)")
    fig_g = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=qol_after,
        number={"suffix": " / 100"},
        delta={"reference": BASE_QOL, "increasing": {"color": "#2ecc71"}, "decreasing": {"color": "#e74c3c"}},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#34495e"},
            "steps": [
                {"range": [0, 40]},
                {"range": [40, 70]},
                {"range": [70, 100]},
            ],
        },
        title={"text": "QoL index (mock)"}
    ))
    fig_g.update_layout(margin=dict(l=10, r=10, t=30, b=10), height=320, template="plotly_white")
    st.plotly_chart(fig_g, use_container_width=True)

# ---------------------------
# Transparency
# ---------------------------
with st.expander("How this demo works"):
    st.markdown(f"""
- **Per bench effects**: +2 Social interactions, +1 Physical activity, −2 Safety.
- **QoL contributions** use equal weights (2, 2, 2) → for +1 bench: **+4** (Social), **+2** (Physical), **−4** (Environmental).
- Gauge shows a baseline QoL of {BASE_QOL} and the new value (0–100), purely illustrative.
- This is a **conceptual prototype** to communicate relationships, not a causal/predictive model.
""")
