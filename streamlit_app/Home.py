# Home.py
import streamlit as st

st.set_page_config(page_title="Veldhuizen • Local Digital Twin (Concept)", layout="wide")

# --- Header ---
st.title("Veldhuizen • Local Digital Twin (Concept Prototype)")
st.caption(
    "Exploring how a local digital twin could support healthy ageing (65+) in Ede–Veldhuizen by "
    "visualising drivers of Quality of Life and testing simple ‘what-if’ scenarios."
)

# --- Purpose / one-paragraph intro ---
st.markdown(
    """
This prototype turns research on **drivers of Quality of Life (QoL)** into an interactive tool for
**policy exploration**. It focuses on residents **65+** in **Veldhuizen** and organises indicators into four
driver dimensions: **Social**, **Physical**, **Psychological**, and **Environmental**.  
It is a **proof of concept** designed to start conversations and help prioritise where and how to act—**not** a predictive model.
"""
)

# --- How to use ---
st.subheader("What you can do here")
c1, c2 = st.columns(2)
with c1:
    st.markdown(
        """
- **Dashboard** — Compare neighbourhoods across indicators (with Ede average as reference).
- **Map** — See **where** challenges/opportunities cluster via an interactive choropleth.
"""
    )
with c2:
    st.markdown(
        """
- **Drivers diagram** — Explore **interrelations** among key drivers (social ↔ physical ↔ environmental ↔ psychological).
- **Scenarios** — Try a **mock simulation** (e.g., adding benches) to illustrate potential trade-offs and QoL impact.
"""
    )

# Optional quick nav (works on Streamlit >= 1.32). Falls back silently if not available.
try:
    st.divider()
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

# --- Notes & limitations (brief, user-facing) ---
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

# --- What a real Local Digital Twin would add ---
with st.expander("What a future Local Digital Twin could add"):
    st.markdown(
        """
- **More granular & real-time data** (amenities, mobility, green space usage, social participation).
- **Weighted relationships** between drivers, based on evidence.
- **Predictive modelling / ML** to compare interventions and expected QoL gains.
- **Participatory, privacy-by-design** development with residents, social workers, and policymakers.
"""
    )

# --- Links ---
st.divider()
st.subheader("Project links")
st.markdown(
    """
- **Code**: https://github.com/ludovicapiccioli/digital_twin_veldhuizen/tree/main/streamlit_app  
- **Data sources**: see the *Data sources* page and report appendix (variables by dimension).  
"""
)

st.caption("Built with QGIS & Streamlit • Team 3538 • ACT 2025")
