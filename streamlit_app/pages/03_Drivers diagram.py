# pages/03_Drivers diagram.py
import streamlit as st
st.set_page_config(page_title="Drivers Diagram", page_icon="🧩", layout="wide")

st.title("Drivers Diagram — Interrelations across Dimensions")
st.caption("SVG replica with pill bubbles and complete arrows, aligned to the reference figure.")

PINK   = "#ff69b4"   # Social
ORANGE = "#f39c12"   # Psychological
GREEN  = "#27ae60"   # Environmental
BLUE   = "#3498db"   # Physical
TEXT   = "#5b6770"

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

  <!-- Frames (more breathing room) -->
  <rect class="frame" x="70"  y="60"  width="420" height="290" stroke="{PINK}"/>
  <text class="title" x="100" y="105" fill="{PINK}">SOCIAL</text>

  <rect class="frame" x="70"  y="390" width="420" height="290" stroke="{ORANGE}"/>
  <text class="title" x="100" y="435" fill="{ORANGE}">Psychological</text>

  <rect class="frame" x="630" y="60"  width="420" height="290" stroke="{GREEN}"/>
  <text class="title" x="660" y="105" fill="{GREEN}">ENVIRONMENTAL</text>

  <rect class="frame" x="630" y="390" width="420" height="290" stroke="{BLUE}"/>
  <text class="title" x="660" y="435" fill="{BLUE}">Physical</text>

  <!-- SOCIAL pills (centered) -->
  <!-- SN pill center: (290, 185)  | CP pill center: (305, 250) -->
  <g id="social">
    <rect class="pill" x="180" y="165" width="220" height="40" fill="{PINK}"/>
    <text class="label" x="290" y="191" text-anchor="middle">Social Networks</text>

    <rect class="pill" x="170" y="230" width="270" height="40" fill="{PINK}"/>
    <text class="label" x="305" y="256" text-anchor="middle">Community participation</text>
  </g>

  <!-- PSYCHOLOGICAL pills -->
  <!-- ES(290,505), SA(290,555), P(300,605), D(290,655) -->
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

  <!-- ENVIRONMENTAL pills (evenly spaced) -->
  <!-- PS(880,165), GS(870,215), MA(865,265), SI(870,315), S(890,365) -->
  <g id="env">
    <rect class="pill" x="730" y="145" width="300" height="40" fill="{GREEN}"/>
    <text class="label" x="880" y="171" text-anchor="middle">Proximity to services</text>

    <rect class="pill" x="740" y="195" width="280" height="40" fill="{GREEN}"/>
    <text class="label" x="880" y="221" text-anchor="middle">Green spaces</text>

    <rect class="pill" x="730" y="245" width="300" height="40" fill="{GREEN}"/>
    <text class="label" x="880" y="271" text-anchor="middle">Mobility &amp; Accessibility</text>

    <rect class="pill" x="740" y="295" width="280" height="40" fill="{GREEN}"/>
    <text class="label" x="880" y="321" text-anchor="middle">Social infrastructures</text>

    <rect class="pill" x="800" y="345" width="220" height="40" fill="{GREEN}"/>
    <text class="label" x="910" y="371" text-anchor="middle">Safety</text>
  </g>

  <!-- PHYSICAL pill -->
  <!-- center (840, 585) -->
  <g id="phys">
    <rect class="pill" x="690" y="565" width="300" height="44" fill="{BLUE}"/>
    <text class="label" x="840" y="592" text-anchor="middle">Physical activity &amp; active lifestyle</text>
  </g>

  <!-- ====== ARROWS (complete set) ====== -->
  <!-- Helper: Social targets -->
  <!-- SN tip: ~ (290,185) ; CP tip: ~ (305,250) -->

  <!-- Environmental → Social Networks (5) -->
  <path d="M730,165 C600,150 440,160 310,180" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M740,215 C610,205 440,175 310,182" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M730,265 C600,250 440,188 310,186" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M740,315 C610,300 440,198 310,190" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M800,365 C650,350 460,205 312,194" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- Environmental → Community participation (5) -->
  <path d="M730,165 C600,165 470,235 430,250" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M740,215 C610,215 480,245 430,255" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M730,265 C600,265 480,258 430,260" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M740,315 C610,318 490,270 430,266" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M800,365 C660,372 520,285 430,274" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- Environmental → Psychological (3) -->
  <!-- to Emotional security(290,505), Sense of autonomy(290,555), Downshift(290,655) -->
  <path d="M740,215 C700,260 520,470 330,505" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M730,265 C680,300 510,520 330,555" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M740,315 C700,360 520,590 330,655" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- Environmental (Safety) → Physical activity -->
  <path d="M910,365 C900,450 875,525 840,570" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- Psychological → Community participation (4 upward) -->
  <path d="M290,505 C295,465 300,330 300,270" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>
  <path d="M290,555 C295,515 300,335 300,272" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>
  <path d="M300,605 C300,565 302,345 300,274" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>

  <!-- Downshift → Physical activity -->
  <path d="M290,655 C460,640 660,615 730,595" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>
</svg>
"""

st.components.v1.html(svg, height=780, scrolling=False)

with st.expander("Notes / tweak tips"):
    st.markdown("""
- Pills are **centered** inside frames, with extra margins to stop crowding.
- The arrow set now matches the reference: Environmental→(Social, Psych, Physical), Psychological→Community participation, and Downshift→Physical.
- If any curve needs a tiny nudge, adjust the numbers in that path’s `C` control segment.
""")
