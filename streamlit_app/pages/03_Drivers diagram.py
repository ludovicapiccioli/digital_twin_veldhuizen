# pages/03_Drivers diagram.py
import streamlit as st

st.set_page_config(page_title="Drivers Diagram", page_icon="🧩", layout="wide")
st.title("Drivers Diagram — Interrelations across Dimensions")
st.caption("SVG replica with colored pill bubbles and curved arrows, aligned to the report figure.")

PINK   = "#ff69b4"   # Social
ORANGE = "#f39c12"   # Psychological
GREEN  = "#27ae60"   # Environmental
BLUE   = "#3498db"   # Physical
TEXT   = "#5b6770"

svg = f"""
<svg viewBox="0 0 1100 740" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Drivers diagram">
  <defs>
    <!-- arrowheads -->
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
      .pill {{ rx: 22; ry: 22; stroke: #fff; stroke-width: 3; }}
      .ghost {{ font: 600 15px 'Inter','Segoe UI',system-ui,-apple-system,sans-serif; fill: {TEXT}; opacity:.9; }}
    ]]></style>
  </defs>

  <!-- === Dimension frames (wider spacing) === -->
  <rect class="frame" x="70"  y="60"  width="400" height="280" stroke="{PINK}"/>
  <text class="title" x="100" y="100" fill="{PINK}">SOCIAL</text>

  <rect class="frame" x="70"  y="390" width="400" height="270" stroke="{ORANGE}"/>
  <text class="title" x="100" y="430" fill="{ORANGE}">Psychological</text>

  <rect class="frame" x="630" y="60"  width="400" height="280" stroke="{GREEN}"/>
  <text class="title" x="660" y="100" fill="{GREEN}">ENVIRONMENTAL</text>

  <rect class="frame" x="630" y="390" width="400" height="270" stroke="{BLUE}"/>
  <text class="title" x="660" y="430" fill="{BLUE}">Physical</text>

  <!-- === SOCIAL pills (centered within frame) === -->
  <g id="social">
    <rect class="pill" x="160" y="165" width="230" height="44" fill="{PINK}"/>
    <text class="label" x="275" y="192" text-anchor="middle">Social Networks</text>

    <rect class="pill" x="160" y="230" width="270" height="44" fill="{PINK}"/>
    <text class="label" x="295" y="257" text-anchor="middle">Community participation</text>
  </g>

  <!-- === PSYCHOLOGICAL pills (stacked neatly) === -->
  <g id="psy">
    <rect class="pill" x="160" y="470" width="240" height="44" fill="{ORANGE}"/>
    <text class="label" x="280" y="497" text-anchor="middle">Emotional security</text>

    <rect class="pill" x="160" y="520" width="240" height="44" fill="{ORANGE}"/>
    <text class="label" x="280" y="547" text-anchor="middle">Sense of autonomy</text>

    <rect class="pill" x="200" y="570" width="200" height="44" fill="{ORANGE}"/>
    <text class="label" x="300" y="597" text-anchor="middle">Purpose</text>

    <rect class="pill" x="160" y="620" width="240" height="44" fill="{ORANGE}"/>
    <text class="label" x="280" y="647" text-anchor="middle">Downshift</text>
  </g>

  <!-- === ENVIRONMENTAL pills (right, evenly spaced) === -->
  <g id="env">
    <rect class="pill" x="690" y="145" width="300" height="44" fill="{GREEN}"/>
    <text class="label" x="840" y="172" text-anchor="middle">Proximity to services</text>

    <rect class="pill" x="720" y="195" width="270" height="44" fill="{GREEN}"/>
    <text class="label" x="855" y="222" text-anchor="middle">Green spaces</text>

    <rect class="pill" x="700" y="245" width="290" height="44" fill="{GREEN}"/>
    <text class="label" x="845" y="272" text-anchor="middle">Mobility &amp; Accessibility</text>

    <rect class="pill" x="720" y="295" width="270" height="44" fill="{GREEN}"/>
    <text class="label" x="855" y="322" text-anchor="middle">Social infrastructures</text>

    <rect class="pill" x="800" y="345" width="190" height="44" fill="{GREEN}"/>
    <text class="label" x="895" y="372" text-anchor="middle">Safety</text>
  </g>

  <!-- === PHYSICAL pill (centered) === -->
  <g id="phys">
    <rect class="pill" x="690" y="560" width="300" height="48" fill="{BLUE}"/>
    <text class="label" x="840" y="589" text-anchor="middle">Physical activity &amp; active lifestyle</text>
  </g>

  <!-- ====== ARROWS (curved Beziers) ====== -->

  <!-- Environmental → Social Networks (five) -->
  <path d="M990,167 C800,150 510,158 385,184" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M990,217 C800,200 520,205 380,193" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M990,267 C800,250 520,232 382,205" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M990,317 C800,300 520,276 386,216" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M990,367 C800,350 520,300 390,226" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- Environmental → Community participation (five) -->
  <path d="M990,167 C790,165 525,225 430,250" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M990,217 C790,215 535,245 430,255" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M990,267 C790,265 535,265 430,260" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M990,317 C790,320 540,285 430,266" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M990,367 C820,380 560,300 430,275" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- Environmental → Psychological (to 3 pills) -->
  <path d="M990,217 C910,240 760,430 400,492" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M990,267 C900,300 750,460 400,542" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M990,317 C890,360 730,510 400,642" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- Environmental → Physical activity (from Safety) -->
  <path d="M895,367 C890,450 875,520 840,560" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- Psychological → Community participation (all four upward) -->
  <path d="M280,492 C290,455 300,320 300,274" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>
  <path d="M280,542 C288,505 298,333 300,276" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>
  <path d="M300,592 C300,555 300,345 300,278" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>
  <path d="M280,642 C360,640 620,610 690,590" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>

  <!-- Optional dotted Social → Environmental arc -->
  <!-- <path d="M320,140 C480,60 800,60 980,140" stroke="{PINK}" stroke-width="4" fill="none" stroke-dasharray="6 8"/> -->
</svg>
"""

st.components.v1.html(svg, height=760, scrolling=False)

with st.expander("Notes / tweak tips"):
    st.markdown("""
- Pills are centered inside each frame so nothing touches the borders.
- I added all **missing arrows** from the reference: Env→Social (both pills), Env→Psych (3 targets), Env→Physical, Psych→Community participation (4 sources), and Downshift→Physical.
- To fine-tune any curve: edit its `path` `C` control points. To move a pill, change the `x`,`y` (and the text x/y just below it).
- Want hover highlight or tooltips? We can add a tiny bit of JS to this SVG while keeping it Streamlit-Cloud friendly.
""")
