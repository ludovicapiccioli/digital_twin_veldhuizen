# Home.py
import streamlit as st

st.set_page_config(page_title="Concept prototype for a DT for Ede-Veldhuizen")

# ---------- Simple CSS for colored blocks ----------
st.markdown("""
<style>
:root{
  --green:#AFC9A0;        /* lighter, faded green */
  --orange:#E3702A;
  --blue:#1E5A7B;
  --card-green:#2E6A2A;
  --card-yellow:#F3C34C;
  --card-peach:#F1C3AC;
  --radius:22px;
}
.block {
  border-radius: var(--radius);
  padding: 22px 26px;
  margin: 8px 0 18px 0;
}
.hero {
  background: var(--green);
  color: #000;           /* black text */
}
.hero h1 {
  color: #000;           /* ensure title text is black */
  margin-top: 0;
}
.section {
  background: var(--orange);
  color:#fff;
}
.section h2, .hero h1 { margin-top: 0; }
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  margin-top: 10px;
}
.card {
  border-radius: 18px;
  padding: 16px 18px;
  min-height: 110px;
  display:flex; flex-direction:column; justify-content:center;
}
.card h4{ margin:0 0 6px 0; color:#fff; }
.card p{ margin:0; color:#f6f6f6; }
.card a{ color:#fff; text-decoration: underline; }
.card-green   { background: var(--card-green); }
.card-blue    { background: var(--blue); }
.card-peach   { background: var(--card-peach); color:#1b1b1b; }
.card-peach h4, .card-peach p, .card-peach a{ color:#1b1b1b; }
.card-yellow  { background: var(--card-yellow); color:#1b1b1b; }
.card-yellow h4, .card-yellow p, .card-yellow a{ color:#1b1b1b; }
.caption { opacity:.9; font-size:0.95rem; }
</style>
""", unsafe_allow_html=True)

# ---------- Header in a faded green block ----------
st.markdown(f"""
<div class="block hero">
  <h1>Concept prototype for a Digital Twin for Ede-Veldhuizen</h1>
  <p class="caption">
    Exploring how a local digital twin could support healthy ageing (65+) in Ede–Veldhuizen by
    visualising drivers of Quality of Life and testing simple ‘what-if’ scenarios.
  </p>
  <p>
    This prototype turns research on <b>drivers of Quality of Life (QoL)</b> into an interactive tool for
    <b>policy exploration</b>. It focuses on residents <b>65+</b> in <b>Veldhuizen</b> and organises indicators into four
    driver dimensions: <b>Social</b>, <b>Physical</b>, <b>Psychological</b>, and <b>Environmental</b>.
    It is a <b>proof of concept</b> designed to start conversations and help prioritise where and how to act—<b>not</b> a predictive model.
  </p>
</div>
""", unsafe_allow_html=True)

# ---------- What you can do here (orange block with four cards) ----------
st.markdown("""
<div class="block section">
  <h2>What you can do here</h2>
  <div class="grid">
    <div class="card card-green">
      <h4>📊 Dashboard</h4>
      <p>Compare <a href="#">neighbourhoods</a> across indicators (Ede average as reference).</p>
    </div>
    <div class="card card-blue">
      <h4>🧩 Drivers diagram</h4>
      <p>Explore interrelations among key drivers (social ↔ physical ↔ environmental ↔ psychological).</p>
    </div>
    <div class="card card-peach">
      <h4>🗺️ Map</h4>
      <p>See where challenges/opportunities cluster via an interactive choropleth.</p>
    </div>
    <div class="card card-yellow">
      <h4>🎛️ Scenarios</h4>
      <p>Try a mock simulation (e.g., adding benches) to illustrate potential trade-offs and QoL impact.</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------- Quick navigation ----------
try:
    st.subheader("Quick navigation")
    nav1, nav2, nav3, nav4 = st.columns(4)
    with nav1:
        st.page_link("pages/01_Dashboard.py", label="📊 Dashboard")
    with nav2:
        st.page_link("pages/02_Map.py", label="🗺️ Map")
    with nav3:
        st.page_link("pages/03_Drivers diagram.py", label="🧩 Drivers")
    with nav4:
        st.page_link("pages/04_Scenarios.py", label="🎛️ Scenarios")
except Exception:
    pass

# ---------- Notes & limitations ----------
st.divider()
st.subheader("About the data & limitations")
st.info(
    "Data sources: CBS **Wijken en Buurten 2024**, RIVM **Gezondheid per wijk en buurt 2022** "
    "and CBS **Nabijheid voorzieningen 2022** (neighbourhood/municipality level). "
    "Health indicators are filtered to **65+** where available."
)
st.warning(
    "This is an **early prototype**. Indicators are **static** and **selected** (not exhaustive); "
    "some relevant variables (e.g., benches, detailed community participation, micro-safety) are not yet available. "
    "The **Scenarios** page uses simplified mock relationships for communication only."
)

# ---------- What a real Local Digital Twin would add ----------
with st.expander("What a future Local Digital Twin could add"):
    st.markdown(
        """
- **More granular & real-time data** (amenities, mobility, green space usage, social participation).
- **Weighted relationships** between drivers, based on evidence.
- **Predictive modelling / ML** to compare interventions and expected QoL gains.
- **Participatory, privacy-by-design** development with residents, social workers, and policymakers.
"""
    )

# ---------- Links ----------
st.divider()
st.subheader("Project links")
st.markdown(
    """
- **Code**: https://github.com/ludovicapiccioli/digital_twin_veldhuizen/tree/main/streamlit_app  
- **Data sources**: see the *Data sources* page and report appendix (variables by dimension).  
"""
)

st.caption("Built with QGIS & Streamlit • Team 3538 • ACT 2025")
