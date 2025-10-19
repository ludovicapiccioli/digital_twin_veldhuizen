# pages/03_Drivers diagram.py
import streamlit as st
st.set_page_config(page_title="Drivers Diagram", page_icon="🧩", layout="wide")

st.title("DRAFT!! Drivers Diagram — Interrelations across Dimensions")
st.caption("draft")

PINK   = "#ff69b4"   # Social-origin / pink arrows
ORANGE = "#f39c12"   # Psychological frame/pills
GREEN  = "#27ae60"   # Environmental-origin / green arrows
BLUE   = "#3498db"   # Physical frame/pill

svg = f"""
<svg viewBox="0 0 1140 820" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Drivers diagram">
  <defs>
    <marker id="arrow-green" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 z" fill="{GREEN}"/>
    </marker>
    <marker id="arrow-pink" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 z" fill="{PINK}"/>
    </marker>
    <!-- NEW: fixed 150° orientation (30° upward from left) for A01 only -->
    <marker id="arrow-pink-150" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="150" markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 z" fill="{PINK}"/>
    </marker>
    <style><![CDATA[
      .frame {{ fill: none; stroke-width: 4; rx: 20; ry: 20; }}
      .label {{ font: 700 16px 'Inter','Segoe UI',system-ui,-apple-system,sans-serif; fill: #fff; }}
      .pill  {{ rx: 22; ry: 22; stroke: #fff; stroke-width: 3; }}
      .titleV {{ font: 800 22px 'Inter','Segoe UI',system-ui,-apple-system,sans-serif; }}
    ]]></style>
  </defs>

  <!-- Frames with vertical titles OUTSIDE -->
  <rect class="frame" x="80"  y="90"  width="440" height="280" stroke="{PINK}"/>
  <text class="titleV" x="60"  y="230" fill="{PINK}" transform="rotate(-90 60 230)">SOCIAL</text>

  <rect class="frame" x="80"  y="410" width="440" height="280" stroke="{ORANGE}"/>
  <text class="titleV" x="60"  y="650" fill="{ORANGE}" transform="rotate(-90 60 650)">Psychological</text>

  <rect class="frame" x="640" y="70"  width="440" height="310" stroke="{GREEN}"/>
  <text class="titleV" x="1090" y="130" fill="{GREEN}" transform="rotate(90 1090 130)">ENVIRONMENTAL</text>

  <rect class="frame" x="640" y="400" width="440" height="310" stroke="{BLUE}"/>
  <text class="titleV" x="1090" y="555" fill="{BLUE}" transform="rotate(90 1090 555)">Physical</text>

  <!-- SOCIAL pills -->
  <g id="social">
    <rect class="pill" x="190" y="175" width="220" height="40" fill="{PINK}"/>
    <text class="label" x="300" y="201" text-anchor="middle">Social Networks</text>

    <rect class="pill" x="180" y="240" width="280" height="40" fill="{PINK}"/>
    <text class="label" x="320" y="266" text-anchor="middle">Community participation</text>
  </g>

  <!-- PSYCHOLOGICAL pills -->
  <g id="psy">
    <rect class="pill" x="180" y="470" width="240" height="40" fill="{ORANGE}"/>
    <text class="label" x="300" y="496" text-anchor="middle">Emotional security</text>

    <rect class="pill" x="180" y="520" width="240" height="40" fill="{ORANGE}"/>
    <text class="label" x="300" y="546" text-anchor="middle">Sense of autonomy</text>

    <rect class="pill" x="200" y="570" width="210" height="40" fill="{ORANGE}"/>
    <text class="label" x="305" y="596" text-anchor="middle">Purpose</text>

    <rect class="pill" x="180" y="620" width="240" height="40" fill="{ORANGE}"/>
    <text class="label" x="300" y="646" text-anchor="middle">Downshift</text>
  </g>

  <!-- ENVIRONMENTAL pills (raised; all inside) -->
  <g id="env">
    <rect class="pill" x="740" y="120" width="300" height="40" fill="{GREEN}"/>
    <text class="label" x="890" y="146" text-anchor="middle">Proximity to services</text>

    <rect class="pill" x="750" y="165" width="280" height="40" fill="{GREEN}"/>
    <text class="label" x="890" y="191" text-anchor="middle">Green spaces</text>

    <rect class="pill" x="740" y="210" width="300" height="40" fill="{GREEN}"/>
    <text class="label" x="890" y="236" text-anchor="middle">Mobility &amp; Accessibility</text>

    <rect class="pill" x="750" y="255" width="280" height="40" fill="{GREEN}"/>
    <text class="label" x="890" y="281" text-anchor="middle">Social infrastructures</text>

    <rect class="pill" x="700" y="300" width="240" height="40" fill="{GREEN}"/>
    <text class="label" x="820" y="326" text-anchor="middle">Safety</text>
  </g>

  <!-- PHYSICAL pill -->
  <g id="phys">
    <rect class="pill" x="700" y="575" width="320" height="44" fill="{BLUE}"/>
    <text class="label" x="860" y="602" text-anchor="middle">Physical activity &amp; active lifestyle</text>
  </g>

  <!-- Dotted Social → Environmental (meta-arc, raised to clear ENV title) -->
  <path id="A00_Social_to_Env_arc"
        d="M120,85 C410,20 820,20 1080,85"
        stroke="{PINK}" stroke-width="3" stroke-dasharray="6 8" fill="none"
        marker-end="url(#arrow-pink)"/>

  <!-- ========= ARROWS ========= -->

  <!-- PINK (Social-origin) — SN arrows start AND end on LEFT edges -->
  <!-- A01 ONLY: fixed 150° arrowhead -->
  <path id="A01_SN_to_Purpose"
        d="M194,195 C60,190 115,560 200,590"
        stroke="{PINK}" stroke-width="3" fill="none" marker-end="url(#arrow-pink-150)"/>

  <!-- The rest keep orient='auto' via arrow-pink -->
  <path id="A02_SN_to_ES"
        d="M194,195 C110,230 130,395 180,490"
        stroke="{PINK}" stroke-width="3" fill="none" marker-end="url(#arrow-pink)"/>
  <path id="A03_SN_to_SA"
        d="M194,195 C90,210 120,440 180,540"
        stroke="{PINK}" stroke-width="3" fill="none" marker-end="url(#arrow-pink)"/>

  <!-- PINK (Community participation origins) -->
  <path id="A04_CP_to_Purpose"
        d="M456,260 C470,340 440,540 410,590"
        stroke="{PINK}" stroke-width="3" fill="none" marker-end="url(#arrow-pink)"/>
  <path id="A05_CP_to_Downshift"
        d="M456,260 C490,390 450,610 420,640"
        stroke="{PINK}" stroke-width="3" fill="none" marker-end="url(#arrow-pink)"/>
  <path id="A06_CP_to_Physical"
        d="M456,260 C560,330 640,560 704,595"
        stroke="{PINK}" stroke-width="3" fill="none" marker-end="url(#arrow-pink)"/>

  <!-- GREEN (Environmental-origin) -->
  <path id="A07_PS_to_SN"
        d="M740,140 C615,125 480,135 406,195"
        stroke="{GREEN}" stroke-width="3" fill="none" marker-end="url(#arrow-green)"/>
  <path id="A08_PS_to_SA"
        d="M740,140 C690,180 520,470 420,520"
        stroke="{GREEN}" stroke-width="3" fill="none" marker-end="url(#arrow-green)"/>
  <path id="A09_GS_to_CP"
        d="M750,185 C620,190 535,255 456,260"
        stroke="{GREEN}" stroke-width="3" fill="none" marker-end="url(#arrow-green)"/>
  <path id="A10_GS_to_Downshift"
        d="M750,185 C680,240 520,575 420,640"
        stroke="{GREEN}" stroke-width="3" fill="none" marker-end="url(#arrow-green)"/>
  <path id="A11_MA_to_CP"
        d="M740,230 C610,235 535,268 456,260"
        stroke="{GREEN}" stroke-width="3" fill="none" marker-end="url(#arrow-green)"/>
  <path id="A12_SI_to_SN"
        d="M750,275 C620,265 490,190 406,195"
        stroke="{GREEN}" stroke-width="3" fill="none" marker-end="url(#arrow-green)"/>
  <path id="A13_SI_to_CP"
        d="M750,275 C620,280 535,280 456,260"
        stroke="{GREEN}" stroke-width="3" fill="none" marker-end="url(#arrow-green)"/>
  <path id="A14_S_to_CP"
        d="M700,320 C610,330 540,300 456,260"
        stroke="{GREEN}" stroke-width="3" fill="none" marker-end="url(#arrow-green)"/>
  <path id="A15_S_to_Downshift"
        d="M700,320 C640,380 510,600 420,640"
        stroke="{GREEN}" stroke-width="3" fill="none" marker-end="url(#arrow-green)"/>
  <path id="A16_ENV_to_Physical"
        d="M880,360 C860,440 800,520 704,595"
        stroke="{GREEN}" stroke-width="3" fill="none" marker-end="url(#arrow-green)"/>
</svg>
"""

st.components.v1.html(svg, height=840, scrolling=False)
