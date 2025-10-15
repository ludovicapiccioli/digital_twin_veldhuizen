# pages/04_Scenarios.py
import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Scenarios • Veldhuizen", page_icon="🧪", layout="wide")

st.title("Scenario Sandbox (Concept Demo)")
st.caption(
    "Interactive, mock relationships between small interventions and QoL. "
    "This is a demonstration, not a predictive model."
)

# ----------------------------
# 1) Mock model configuration
# ----------------------------
BASELINE_FACTORS = {
    "social_interactions": 60,   # Social dimension proxy
    "physical_activity": 55,     # Physical dimension proxy
    "safety": 50,                # Environmental dimension proxy
}

# Emphasize Social & Environmental
DIM_WEIGHTS = {"social": 0.40, "physical": 0.20, "environmental": 0.40}

# Factor → dimension mapping (kept 1:1 for clarity)
DIMENSION_FACTORS = {
    "social": ["social_interactions"],
    "physical": ["physical_activity"],
    "environmental": ["safety"],
}

# Linear mock effects per intervention unit 
INTERVENTION_WEIGHTS = {
    "benches": {"social_interactions": 2.0, "physical_activity": 1.0, "safety": 0.5},
    "lighting": {"safety": 2.5, "social_interactions": 0.5, "physical_activity": 0.5},
    "community_events": {"social_interactions": 3.0, "safety": 0.3},
}
INTERVENTION_RANGES = {"benches": (-10, 10), "lighting": (-10, 10), "community_events": (-10, 10)}
FACTOR_MIN, FACTOR_MAX = 0, 100

# -------------
# Helpers
# -------------
def apply_interventions(baseline: dict, deltas: dict, non_linear=False) -> dict:
    """Apply slider deltas via weight matrix; optional gentle diminishing returns."""
    factors = baseline.copy()
    for itv, delta in deltas.items():
        if delta == 0:
            continue
        for factor, w in INTERVENTION_WEIGHTS.get(itv, {}).items():
            factors[factor] = factors.get(factor, 0) + (delta * w)

    if non_linear:
        # Soft cap using tanh around 50
        for k, v in factors.items():
            x = (v - 50) / 25.0
            factors[k] = np.tanh(x) * 25 + 50

    # Clamp to 0..100
    for k in factors:
        factors[k] = float(np.clip(factors[k], FACTOR_MIN, FACTOR_MAX))
    return factors

def aggregate_dimensions(factors: dict) -> dict:
    return {dim: float(np.mean([factors[f] for f in facs])) for dim, facs in DIMENSION_FACTORS.items()}

def qol_score(dimensions: dict) -> float:
    return sum(dimensions[d] * DIM_WEIGHTS[d] for d in DIM_WEIGHTS)

# ----------------------------
# 2) UI – Presets & sliders
# ----------------------------
st.subheader("Configure scenario")

if "itv" not in st.session_state:
    st.session_state.itv = {"benches": 0, "lighting": 0, "community_events": 0}
if "non_linear" not in st.session_state:
    st.session_state.non_linear = False

def set_preset(values, non_linear=False):
    st.session_state.itv = values
    st.session_state.non_linear = non_linear

c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("Baseline"):
        set_preset({"benches": 0, "lighting": 0, "community_events": 0}, False)
with c2:
    if st.button("Active neighbourhood"):
        set_preset({"benches": 6, "lighting": 2, "community_events": 2}, False)
with c3:
    if st.button("Safe & social"):
        set_preset({"benches": 3, "lighting": 8, "community_events": 5}, False)
with c4:
    if st.button("Gentle non-linearity"):
        set_preset({"benches": 3, "lighting": 8, "community_events": 5}, True)

with st.expander("Manual adjustments", expanded=True):
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.session_state.itv["benches"] = st.slider("Benches (Δ units)",
            *INTERVENTION_RANGES["benches"], value=st.session_state.itv["benches"])
    with s2:
        st.session_state.itv["lighting"] = st.slider("Lighting (Δ segments)",
            *INTERVENTION_RANGES["lighting"], value=st.session_state.itv["lighting"])
    with s3:
        st.session_state.itv["community_events"] = st.slider("Community events (Δ / month)",
            *INTERVENTION_RANGES["community_events"], value=st.session_state.itv["community_events"])
    with s4:
        st.session_state.non_linear = st.checkbox(
            "Apply gentle diminishing returns", value=st.session_state.non_linear
        )

# ----------------------------
# 3) Compute results
# ----------------------------
baseline_dims = aggregate_dimensions(BASELINE_FACTORS)
baseline_qol = qol_score(baseline_dims)

factors_after = apply_interventions(BASELINE_FACTORS, st.session_state.itv, st.session_state.non_linear)
dims_after = aggregate_dimensions(factors_after)
qol_after = qol_score(dims_after)

delta_qol = qol_after - baseline_qol
pct_qol = (delta_qol / baseline_qol * 100) if baseline_qol else 0

# ----------------------------
# 4) KPIs & narrative
# ----------------------------
st.subheader("Impact overview")
k1, k2, k3, k4 = st.columns(4)
k1.metric("QoL (0–100)", f"{qol_after:0.1f}", f"{delta_qol:+0.1f}")
k2.metric("Social dim.", f"{dims_after['social']:0.1f}",
          f"{dims_after['social']-baseline_dims['social']:+0.1f}")
k3.metric("Environmental dim.", f"{dims_after['environmental']:0.1f}",
          f"{dims_after['environmental']-baseline_dims['environmental']:+0.1f}")
k4.metric("Physical dim.", f"{dims_after['physical']:0.1f}",
          f"{dims_after['physical']-baseline_dims['physical']:+0.1f}")

st.write(
    f"**Scenario summary:** Benches {st.session_state.itv['benches']:+d}, "
    f"Lighting {st.session_state.itv['lighting']:+d}, "
    f"Community events {st.session_state.itv['community_events']:+d}. "
    f"This mock scenario changes QoL by **{delta_qol:+0.1f}** points ({pct_qol:+0.1f}%)."
)

# ----------------------------
# 5) Before/After charts
# ----------------------------
st.subheader("Before vs. After")

dim_df = pd.DataFrame({"Baseline": baseline_dims, "Scenario": dims_after})
dim_df = dim_df.loc[["social", "environmental", "physical"]]
dim_df.index = ["Social", "Environmental", "Physical"]
st.bar_chart(dim_df)

qol_df = pd.DataFrame({"Baseline": [baseline_qol], "Scenario": [qol_after]}, index=["QoL"])
st.bar_chart(qol_df)

# ----------------------------
# 6) Transparency box
# ----------------------------
with st.expander("What’s under the hood (prototype logic)"):
    st.markdown("""
- **Concept demo** with linear, hand-tuned relationships (not predictive).
- Factors → dimensions (simple proxies): Social interactions → Social; Safety → Environmental; Physical activity → Physical.
- QoL = Social 0.40 + Environmental 0.40 + Physical 0.20.
- Interventions adjust factors per unit; scores are clamped 0–100.
- Optional **diminishing returns** via a gentle `tanh` transform.
""")
