# pages/03_Drivers diagram.py
import streamlit as st

st.set_page_config(page_title="Drivers Diagram", page_icon="🧩", layout="wide")
st.title("Drivers Diagram — Interrelations across Dimensions")
st.caption("Static SVG replica with colored pill bubbles and curved arrows (concept demo).")

PINK   = "#ff69b4"   # Social
ORANGE = "#f39c12"   # Psychological
GREEN  = "#27ae60"   # Environmental
BLUE   = "#3498db"   # Physical
TEXT   = "#5b6770"

svg = f"""
<svg viewBox="0 0 1000 700" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Drivers diagram">
  <defs>
    <!-- arrowheads -->
    <marker id="arrow-green" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 z" fill="{GREEN}"/>
    </marker>
    <marker id="arrow-orange" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 z" fill="{ORANGE}"/>
    </marker>
    <style><![CDATA[
      .frame {{
        fill: none; stroke-width: 3; rx: 14; ry: 14;
      }}
      .title {{
        font: 700 20px 'Inter','Segoe UI',system-ui,-apple-system,sans-serif;
      }}
      .label {{
        font: 600 15px 'Inter','Segoe UI',system-ui,-apple-system,sans-serif;
        fill: #ffffff;
      }}
      .ghost {{
        font: 600 15px 'Inter','Segoe UI',system-ui,-apple-system,sans-serif;
        fill: {TEXT};
      }}
      .pill {{
        rx: 20; ry: 20; stroke: #ffffff; stroke-width: 3;
      }}
    ]]></style>
  </defs>

  <!-- Dimension frames -->
  <rect class="frame" x="80"  y="60"  width="360" height="260" stroke="{PINK}"/>
  <text class="title" x="110" y="95" fill="{PINK}">SOCIAL</text>

  <rect class="frame" x="80"  y="380" width="360" height="260" stroke="{ORANGE}"/>
  <text class="title" x="110" y="415" fill="{ORANGE}">Psychological</text>

  <rect class="frame" x="560" y="60"  width="360" height="260" stroke="{GREEN}"/>
  <text class="title" x="590" y="95" fill="{GREEN}">ENVIRONMENTAL</text>

  <rect class="frame" x="560" y="380" width="360" height="260" stroke="{BLUE}"/>
  <text class="title" x="590" y="415" fill="{BLUE}">Physical</text>

  <!-- SOCIAL pills -->
  <g>
    <rect class="pill" x="200" y="150" width="200" height="40" fill="{PINK}"/>
    <text class="label" x="300" y="176" text-anchor="middle">Social Networks</text>

    <rect class="pill" x="180" y="215" width="220" height="40" fill="{PINK}"/>
    <text class="label" x="290" y="241" text-anchor="middle">Community participation</text>
  </g>

  <!-- PSYCHOLOGICAL pills -->
  <g>
    <rect class="pill" x="170" y="450" width="200" height="40" fill="{ORANGE}"/>
    <text class="label" x="270" y="476" text-anchor="middle">Emotional security</text>

    <rect class="pill" x="170" y="490" width="200" height="40" fill="{ORANGE}"/>
    <text class="label" x="270" y="516" text-anchor="middle">Sense of autonomy</text>

    <rect class="pill" x="200" y="530" width="170" height="40" fill="{ORANGE}"/>
    <text class="label" x="285" y="556" text-anchor="middle">Purpose</text>

    <rect class="pill" x="170" y="590" width="200" height="40" fill="{ORANGE}"/>
    <text class="label" x="270" y="616" text-anchor="middle">Downshift</text>
  </g>

  <!-- ENVIRONMENTAL pills -->
  <g>
    <rect class="pill" x="660" y="135" width="240" height="40" fill="{GREEN}"/>
    <text class="label" x="780" y="161" text-anchor="middle">Proximity to services</text>

    <rect class="pill" x="700" y="175" width="200" height="40" fill="{GREEN}"/>
    <text class="label" x="800" y="201" text-anchor="middle">Green spaces</text>

    <rect class="pill" x="670" y="215" width="230" height="40" fill="{GREEN}"/>
    <text class="label" x="785" y="241" text-anchor="middle">Mobility &amp; Accessibility</text>

    <rect class="pill" x="700" y="255" width="200" height="40" fill="{GREEN}"/>
    <text class="label" x="800" y="281" text-anchor="middle">Social infrastructures</text>

    <rect class="pill" x="770" y="295" width="130" height="40" fill="{GREEN}"/>
    <text class="label" x="835" y="321" text-anchor="middle">Safety</text>
  </g>

  <!-- PHYSICAL pill -->
  <g>
    <rect class="pill" x="615" y="540" width="300" height="44" fill="{BLUE}"/>
    <text class="label" x="765" y="567" text-anchor="middle">Physical activity &amp; active lifestyle</text>
  </g>

  <!-- Soft grey "ghost" text under pills for context (optional) -->
  <!-- <text class="ghost" x="130" y="176">Social Networks</text> -->

  <!-- Curved arrows from ENVIRONMENTAL (green) -->
  <path d="M780,155 C630,135 430,152 300,168" stroke="{GREEN}" stroke-width="4" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M800,195 C640,185 430,205 290,235" stroke="{GREEN}" stroke-width="4" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M785,235 C635,235 430,238 290,232" stroke="{GREEN}" stroke-width="4" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M800,275 C640,285 460,268 290,245" stroke="{GREEN}" stroke-width="4" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M835,315 C700,335 470,300 290,255" stroke="{GREEN}" stroke-width="4" fill="none" marker-end="url(#arrow-green)"/>

  <!-- Environmental to Physical (downwards curved) -->
  <path d="M835,315 C835,420 820,510 765,546" stroke="{GREEN}" stroke-width="4" fill="none" marker-end="url(#arrow-green)"/>

  <!-- Curved arrows from PSYCHOLOGICAL (orange) -->
  <path d="M270,470 C270,430 280,315 290,255" stroke="{ORANGE}" stroke-width="4" fill="none" marker-end="url(#arrow-orange)"/>
  <path d="M270,510 C270,470 280,318 290,255" stroke="{ORANGE}" stroke-width="4" fill="none" marker-end="url(#arrow-orange)"/>
  <path d="M285,550 C285,510 288,322 290,255" stroke="{ORANGE}" stroke-width="4" fill="none" marker-end="url(#arrow-orange)"/>

  <!-- Downshift to Physical -->
  <path d="M270,610 C420,600 620,590 720,560" stroke="{ORANGE}" stroke-width="4" fill="none" marker-end="url(#arrow-orange)"/>
</svg>
"""

st.components.v1.html(svg, height=740, scrolling=False)

with st.expander("Notes / tweak tips"):
    st.markdown("""
- This SVG uses **colored pill bubbles** (`rect` with large `rx/ry`) for each driver.
- To nudge any bubble, adjust its `x`/`y` and (if needed) `width` in the `<rect>` and the `x`/`y` of the following `<text>`.
- Curves are cubic Béziers (`<path ... d="M x1,y1 C cx1,cy1 cx2,cy2 x2,y2">`). Move control points to fine-tune the arc.
- Arrow colors reflect the **source dimension** (green = Environmental, orange = Psychological).
""")
