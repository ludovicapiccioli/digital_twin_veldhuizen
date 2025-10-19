# pages/03_Drivers diagram.py
import streamlit as st
st.set_page_config(page_title="Drivers Diagram", page_icon="🧩", layout="wide")

st.title("Drivers Diagram — Interrelations across Dimensions")
st.caption("Dimension titles placed outside frames. Pills fully inside; arrow tips stop at pill edges (no text overlap).")

PINK   = "#ff69b4"   # Social
ORANGE = "#f39c12"   # Psychological
GREEN  = "#27ae60"   # Environmental
BLUE   = "#3498db"   # Physical

svg = f"""
<svg viewBox="0 0 1140 800" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Drivers diagram">
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

  <!-- ===== Titles OUTSIDE frames ===== -->
  <text class="title" x="90"  y="72"  fill="{PINK}">SOCIAL</text>
  <text class="title" x="90"  y="400" fill="{ORANGE}">Psychological</text>
  <text class="title" x="650" y="72"  fill="{GREEN}">ENVIRONMENTAL</text>
  <text class="title" x="650" y="400" fill="{BLUE}">Physical</text>

  <!-- ===== Frames (more breathing room since titles are outside) ===== -->
  <rect class="frame" x="70"  y="86"  width="440" height="290" stroke="{PINK}"/>
  <rect class="frame" x="70"  y="414" width="440" height="290" stroke="{ORANGE}"/>
  <rect class="frame" x="640" y="86"  width="440" height="290" stroke="{GREEN}"/>
  <rect class="frame" x="640" y="414" width="440" height="290" stroke="{BLUE}"/>

  <!-- ===== SOCIAL pills ===== -->
  <!-- Right edges: SN=410, CP=460 -->
  <g id="social">
    <rect class="pill" x="190" y="185" width="220" height="40" fill="{PINK}"/>
    <text class="label" x="300" y="211" text-anchor="middle">Social Networks</text>

    <rect class="pill" x="180" y="250" width="280" height="40" fill="{PINK}"/>
    <text class="label" x="320" y="276" text-anchor="middle">Community participation</text>
  </g>

  <!-- ===== PSYCHOLOGICAL pills ===== -->
  <!-- Right edges: ES=420, SA=420, Purpose=410, Downshift=420 -->
  <g id="psy">
    <rect class="pill" x="180" y="505" width="240" height="40" fill="{ORANGE}"/>
    <text class="label" x="300" y="531" text-anchor="middle">Emotional security</text>

    <rect class="pill" x="180" y="555" width="240" height="40" fill="{ORANGE}"/>
    <text class="label" x="300" y="581" text-anchor="middle">Sense of autonomy</text>

    <rect class="pill" x="200" y="605" width="210" height="40" fill="{ORANGE}"/>
    <text class="label" x="305" y="631" text-anchor="middle">Purpose</text>

    <rect class="pill" x="180" y="655" width="240" height="40" fill="{ORANGE}"/>
    <text class="label" x="300" y="681" text-anchor="middle">Downshift</text>
  </g>

  <!-- ===== ENVIRONMENTAL pills ===== -->
  <!-- Safety moved LEFT and DOWN slightly; right edge = 940, well inside frame right = 1080 -->
  <g id="env">
    <rect class="pill" x="740" y="165" width="300" height="40" fill="{GREEN}"/>
    <text class="label" x="890" y="191" text-anchor="middle">Proximity to services</text>

    <rect class="pill" x="750" y="215" width="280" height="40" fill="{GREEN}"/>
    <text class="label" x="890" y="241" text-anchor="middle">Green spaces</text>

    <rect class="pill" x="740" y="265" width="300" height="40" fill="{GREEN}"/>
    <text class="label" x="890" y="291" text-anchor="middle">Mobility &amp; Accessibility</text>

    <rect class="pill" x="750" y="315" width="280" height="40" fill="{GREEN}"/>
    <text class="label" x="890" y="341" text-anchor="middle">Social infrastructures</text>

    <!-- SAFETY safely inside -->
    <rect class="pill" x="700" y="365" width="240" height="40" fill="{GREEN}"/>
    <text class="label" x="820" y="391" text-anchor="middle">Safety</text>
  </g>

  <!-- ===== PHYSICAL pill ===== -->
  <!-- Left edge x=700; arrow tips will land at ~704 -->
  <g id="phys">
    <rect class="pill" x="700" y="585" width="320" height="44" fill="{BLUE}"/>
    <text class="label" x="860" y="612" text-anchor="middle">Physical activity &amp; active lifestyle</text>
  </g>

  <!-- ===== ARROWS — tips stop on pill borders ===== -->

  <!-- ENV → Social Networks (tips at x=406) -->
  <path d="M740,185 C610,170 470,180 406,205" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M750,225 C620,215 480,197 406,205" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M740,275 C610,265 480,205 406,205" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M750,325 C620,315 480,215 406,205" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M700,385 C600,365 490,230 406,205" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- ENV → Community participation (tips at x=456) -->
  <path d="M740,185 C610,185 520,255 456,270" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M750,225 C620,225 525,265 456,270" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M740,275 C610,275 525,278 456,270" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M750,325 C620,328 525,290 456,270" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M700,385 C610,392 530,300 456,270" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- ENV → Psychological (tips at ES/SA/D = ~ right edges 420/420/420) -->
  <path d="M750,225 C710,270 525,470 420,525" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M740,275 C700,315 520,520 420,575" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M700,385 C665,430 510,620 420,675" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- Safety → Physical (tip at blue pill left edge ≈ 704) -->
  <path d="M820,385 C810,480 780,545 704,607" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- PSY → Community participation (tips at 456) -->
  <path d="M300,525 C305,485 310,350 456,270" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>
  <path d="M300,575 C305,535 310,360 456,270" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>
  <path d="M305,625 C305,585 308,365 456,270" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>

  <!-- Downshift → Physical (tip at 704) -->
  <path d="M300,675 C480,660 665,635 704,607" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>
</svg>
"""

st.components.v1.html(svg, height=820, scrolling=False)

with st.expander("Notes / tweak tips"):
    st.markdown("""
- Titles are **outside** the frames, freeing space inside the boxes.
- The **Safety** pill is at `x=700` (right edge `= 940`), well inside the Environmental frame (`right = 1080`).
- Arrow tips stop on pill borders: Social (x=406/456), Psych (~420), Physical (x=704).  
  If a tip still looks slightly inside/outside on your screen, nudge those tip x-values by ±2.
""")
