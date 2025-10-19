import streamlit as st
st.set_page_config(page_title="Drivers Diagram", page_icon="🧩", layout="wide")

st.title("Drivers Diagram — Interrelations across Dimensions")
st.caption("Pills are centered inside frames; arrows stop at the pill edge (no text overlap).")

PINK   = "#ff69b4"   # Social
ORANGE = "#f39c12"   # Psychological
GREEN  = "#27ae60"   # Environmental
BLUE   = "#3498db"   # Physical

svg = f"""
<svg viewBox="0 0 1120 760" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow-green" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 z" fill="{GREEN}"/>
    </marker>
    <marker id="arrow-orange" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 z" fill="{ORANGE}"/>
    </marker>
    <style><![CDATA[
      .frame {{ fill: none; stroke-width: 4; rx: 20; ry: 20; }}
      .title {{ font: 800 22px 'Inter','Segoe UI',system-ui,-apple-system,sans-serif; }}
      .label {{ font: 700 16px 'Inter','Segoe UI',system-ui,-apple-system,sans-serif; fill: #fff; }}
      .pill  {{ rx: 22; ry: 22; stroke: #fff; stroke-width: 3; }}
    ]]></style>
  </defs>

  <!-- Frames -->
  <rect class="frame" x="70"  y="60"  width="420" height="290" stroke="{PINK}"/>
  <text class="title" x="100" y="105" fill="{PINK}">SOCIAL</text>

  <rect class="frame" x="70"  y="390" width="420" height="290" stroke="{ORANGE}"/>
  <text class="title" x="100" y="435" fill="{ORANGE}">Psychological</text>

  <rect class="frame" x="630" y="60"  width="420" height="290" stroke="{GREEN}"/>
  <text class="title" x="660" y="105" fill="{GREEN}">ENVIRONMENTAL</text>

  <rect class="frame" x="630" y="390" width="420" height="290" stroke="{BLUE}"/>
  <text class="title" x="660" y="435" fill="{BLUE}">Physical</text>

  <!-- SOCIAL pills (centers at ~ (290,185) and (305,250)) -->
  <g id="social">
    <rect class="pill" x="180" y="165" width="220" height="40" fill="{PINK}"/>
    <text class="label" x="290" y="191" text-anchor="middle">Social Networks</text>

    <rect class="pill" x="170" y="230" width="270" height="40" fill="{PINK}"/>
    <text class="label" x="305" y="256" text-anchor="middle">Community participation</text>
  </g>

  <!-- PSYCHOLOGICAL pills (right edge x=410 for first, second, fourth; 400 for 'Purpose') -->
  <g id="psy">
    <rect class="pill" x="170" y="485" width="240" height="40" fill="{ORANGE}"/>
    <text class="label" x="290" y="511" text-anchor="middle">Emotional security</text>

    <rect class="pill" x="170" y="535" width="240" height="40" fill="{ORANGE}"/>
    <text class="label" x="290" y="561" text-anchor="middle">Sense of autonomy</text>

    <rect class="pill" x="200" y="585" width="200" height="40" fill="{ORANGE}"/>
    <text class="label" x="300" y="611" text-anchor="middle">Purpose</text>

    <rect class="pill" x="170" y="635" width="240" height="40" fill="{ORANGE}"/>
    <text class="label" x="290" y="661" text-anchor="middle">Downshift</text>
  </g>

  <!-- ENVIRONMENTAL pills (Safety moved left to stay inside frame) -->
  <g id="env">
    <rect class="pill" x="730" y="145" width="300" height="40" fill="{GREEN}"/>
    <text class="label" x="880" y="171" text-anchor="middle">Proximity to services</text>

    <rect class="pill" x="740" y="195" width="280" height="40" fill="{GREEN}"/>
    <text class="label" x="880" y="221" text-anchor="middle">Green spaces</text>

    <rect class="pill" x="730" y="245" width="300" height="40" fill="{GREEN}"/>
    <text class="label" x="880" y="271" text-anchor="middle">Mobility &amp; Accessibility</text>

    <rect class="pill" x="740" y="295" width="280" height="40" fill="{GREEN}"/>
    <text class="label" x="880" y="321" text-anchor="middle">Social infrastructures</text>

    <!-- Safety shifted left: right edge now at 980 (< frame right 1050) -->
    <rect class="pill" x="760" y="345" width="220" height="40" fill="{GREEN}"/>
    <text class="label" x="870" y="371" text-anchor="middle">Safety</text>
  </g>

  <!-- PHYSICAL pill (left edge x=690) -->
  <g id="phys">
    <rect class="pill" x="690" y="565" width="300" height="44" fill="{BLUE}"/>
    <text class="label" x="840" y="592" text-anchor="middle">Physical activity &amp; active lifestyle</text>
  </g>

  <!-- ====== ARROWS: tips land on pill edges (not inside) ====== -->

  <!-- Convenience: edge x-positions for arrow tips -->
  <!-- Social right edges: SN=400, CP=440 -->
  <!-- Psych right edges: ES=410, SA=410, Purpose=400, Downshift=410 -->
  <!-- Physical left edge: PA=690 -->

  <!-- Environmental → Social Networks (tip x=396) -->
  <path d="M730,165 C600,150 460,158 396,185" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M740,195 C610,185 470,175 396,185" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M730,245 C600,235 470,182 396,185" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M740,295 C610,285 470,195 396,185" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M760,345 C630,335 480,205 396,185" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- Environmental → Community participation (tip x=436) -->
  <path d="M730,165 C600,165 500,235 436,250" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M740,195 C610,195 505,245 436,250" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M730,245 C600,245 505,258 436,250" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M740,295 C610,298 505,270 436,250" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M760,345 C640,352 520,286 436,250" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- Environmental → Psychological (tips at orange right edges ≈ 408/408/408) -->
  <path d="M740,195 C700,240 520,460 408,505" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M730,245 C690,280 515,515 408,555" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M760,345 C710,395 520,595 408,655" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- Environmental (Safety) → Physical activity (tip at PA left edge ≈ 694) -->
  <path d="M870,365 C860,450 820,525 694,585" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- Psychological → Community participation (tips at 436) -->
  <path d="M290,505 C295,465 300,330 436,250" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>
  <path d="M290,555 C295,515 300,335 436,250" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>
  <path d="M300,605 C300,565 300,345 436,250" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>

  <!-- Downshift → Physical activity (tip at 694) -->
  <path d="M290,655 C460,640 640,615 694,585" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>
</svg>
"""

st.components.v1.html(svg, height=780, scrolling=False)

with st.expander("Notes"):
    st.markdown("""
- **Safety** was shifted left so it stays fully inside the Environmental frame.
- Arrow tips end at the **pill borders** (x=396/436 for Social, x≈408 for Psych, x=694 for Physical).  
  If you want the tips to sit *exactly* on the stroke, nudge those x-values by ±2.
- To tweak any curve, adjust the control point in the cubic Bézier `C` segment.
""")
