# pages/04_Scenarios.py
import streamlit as st

# Page config must be the first Streamlit call in this file
st.set_page_config(page_title="Scenarios • Veldhuizen", page_icon="🧪", layout="wide")

st.title("🧪 Scenario Sandbox — Benches → Drivers → QoL")
st.caption("Concept demo (mock relationships). Adjust benches to see how factors and QoL shift.")

# ---------------------------
# Controls
# ---------------------------
b = st.slider("Add / remove benches (Δ units)", -10, 10, 0, help="Purely illustrative, not predictive.")

# Per-bench effects on factors (from your diagram idea)
delta_social_interactions =  2 * b   # +2 per bench
delta_physical_activity   =  1 * b   # +1 per bench
delta_safety              = -2 * b   # −2 per bench (e.g., perceived nuisance)

# Dimension → QoL weights (positive contributions of dimensions to QoL)
# Set to 2,2,2 so the right-hand contributions resemble your example (+4, +2, −4 for b=+1).
W_SOCIAL = 2
W_PHYS   = 2
W_ENV    = 2  # (safety belongs to environmental; lower safety reduces QoL)

# QoL contributions from each dimension given the factor deltas
qol_from_social = W_SOCIAL * delta_social_interactions
qol_from_phys   = W_PHYS   * delta_physical_activity
qol_from_env    = W_ENV    * delta_safety            # will be negative if safety goes down

qol_total = qol_from_social + qol_from_phys + qol_from_env

# ---------------------------
# Dynamic Graphviz diagram
# ---------------------------
def color(v):      # green for positive, red for negative, grey for zero
    return "#27ae60" if v > 0 else ("#c0392b" if v < 0 else "#7f8c8d")

def fmt(v):        # show sign and integer
    return f"{v:+d}"

# Node labels
bench_label = f"<<B>+{b} Bench</B>>" if b>0 else (f"<<B>{b} Bench</B>>" if b<0 else "<<B>±0 Bench</B>>")
soc_fac_lbl = f"<<B>{fmt(delta_social_interactions)}</B> Social interactions>"
phy_fac_lbl = f"<<B>{fmt(delta_physical_activity)}</B> Physical activity>"
env_fac_lbl = f"<<B>{fmt(delta_safety)}</B> Safety>"

qol_lines = [
    f"{fmt(qol_from_social)} from Social",
    f"{fmt(qol_from_phys)} from Physical",
    f"{fmt(qol_from_env)} from Environmental",
    "—",
    f"<B>Δ QoL = {fmt(qol_total)}</B>",
]
qol_label = "<< " + "<BR/>".join(qol_lines) + " >>"

# Colors
c_soc = color(delta_social_interactions)
c_phy = color(delta_physical_activity)
c_env = color(delta_safety)

edge_pos = "#27ae60"
edge_neg = "#c0392b"

# DOT graph
dot = f"""
digraph G {{
    graph [rankdir=LR, splines=true, nodesep=0.6, ranksep=0.8, bgcolor="white"];
    node  [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=12];
    edge  [penwidth=2, arrowsize=0.8, color="#2c3e50"];

    // Left: intervention
    bench [label={bench_label}, shape=box, fillcolor="#f1c40f", color="#b7950b"];

    // Factor nodes
    social_fac [label={soc_fac_lbl}, fillcolor="#fce9e3", color="#e67e22", fontcolor="#e67e22"];
    phys_fac   [label={phy_fac_lbl}, fillcolor="#e8f1fb", color="#2980b9", fontcolor="#2980b9"];
    env_fac    [label={env_fac_lbl}, fillcolor="#f7e9f5", color="#8e44ad", fontcolor="#8e44ad"];

    // Dimension bubbles (clusters)
    subgraph cluster_social {{
        label="Social dimension";
        color="#fadbd8"; style="rounded,dashed"; penwidth=2; fontname="Helvetica"; fontsize=12;
        social_fac;
    }}

    subgraph cluster_physical {{
        label="Physical dimension";
        color="#d6eaf8"; style="rounded,dashed"; penwidth=2; fontname="Helvetica"; fontsize=12;
        phys_fac;
    }}

    subgraph cluster_environmental {{
        label="Environmental dimension";
        color="#f5eef8"; style="rounded,dashed"; penwidth=2; fontname="Helvetica"; fontsize=12;
        env_fac;
    }}

    // QoL node (right)
    qol [label={qol_label}, shape=box, fillcolor="#b8e994", color="#78e08f", fontsize=12];

    // Edges: Bench -> factors (green/red)
    bench -> social_fac [color="{edge_pos if delta_social_interactions>=0 else edge_neg}"];
    bench -> phys_fac   [color="{edge_pos if delta_physical_activity>=0 else edge_neg}"];
    bench -> env_fac    [color="{edge_pos if delta_safety>=0 else edge_neg}"];

    // Edges: factors -> QoL (always positive contribution of dimensions)
    social_fac -> qol [color="#27ae60"]; // higher social → higher QoL
    phys_fac   -> qol [color="#27ae60"];
    env_fac    -> qol [color="#27ae60"];
}}
"""

st.graphviz_chart(dot, use_container_width=True)

# ---------------------------
# Compact KPIs under the diagram 
# ---------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Δ Social interactions",  fmt(delta_social_interactions))
c2.metric("Δ Physical activity",    fmt(delta_physical_activity))
c3.metric("Δ Safety",               fmt(delta_safety))
c4.metric("Δ QoL (composite)",     fmt(qol_total))

with st.expander("How this mock works"):
    st.markdown(f"""
- Per bench effects on factors: **+2 Social**, **+1 Physical**, **−2 Safety** (you can adjust the slider).
- Dimensions contribute positively to QoL with equal weights (**2, 2, 2**) to mirror your sketch:
  - QoL from Social = 2 × ΔSocial  
  - QoL from Physical = 2 × ΔPhysical  
  - QoL from Environmental = 2 × ΔSafety  
- Because Safety drops when benches increase (in this toy example), the Environmental contribution can be **negative**.
- This is purely illustrative to communicate *cause → factor → dimension → QoL*.
""")
