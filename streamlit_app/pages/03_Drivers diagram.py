# pages/03_Drivers diagram.py
import streamlit as st
st.set_page_config(page_title="Drivers Diagram", page_icon="🧩", layout="wide")

st.title("DRAFT!! Drivers Diagram — Interrelations across Dimensions")
st.caption("draft.")

PINK   = "#ff69b4"   # Social / Social-side arrows
ORANGE = "#f39c12"   # Psychological (kept for the Downshift→Physical + CP links)
GREEN  = "#27ae60"   # Environmental
BLUE   = "#3498db"   # Physical

svg = f"""
<svg viewBox="0 0 1140 820" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Drivers diagram">
  <defs>
    <marker id="arrow-green" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 z" fill="{GREEN}"/>
    </marker>
    <marker id="arrow-orange" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 z" fill="{ORANGE}"/>
    </marker>
    <marker id="arrow-pink" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 z" fill="{PINK}"/>
    </marker>
    <style><![CDATA[
      .frame {{ fill: none; stroke-width: 4; rx: 20; ry: 20; }}
      .label {{ font: 700 16px 'Inter','Segoe UI',system-ui,-apple-system,sans-serif; fill: #fff; }}
      .pill  {{ rx: 22; ry: 22; stroke: #fff; stroke-width: 3; }}
      .titleV {{ font: 800 22px 'Inter','Segoe UI',system-ui,-apple-system,sans-serif; }}
    ]]></style>
  </defs>

  <!-- ===== Frames with vertical titles OUTSIDE ===== -->
  <rect class="frame" x="80"  y="90"  width="440" height="280" stroke="{PINK}"/>
  <text class="titleV" x="60" y="230" fill="{PINK}" transform="rotate(-90 60 230)">SOCIAL</text>

  <rect class="frame" x="80"  y="410" width="440" height="280" stroke="{ORANGE}"/>
  <text class="titleV" x="60" y="550" fill="{ORANGE}" transform="rotate(-90 60 550)">Psychological</text>

  <rect class="frame" x="640" y="70"  width="440" height="310" stroke="{GREEN}"/>
  <text class="titleV" x="1090" y="225" fill="{GREEN}" transform="rotate(90 1090 225)">ENVIRONMENTAL</text>

  <rect class="frame" x="640" y="400" width="440" height="310" stroke="{BLUE}"/>
  <text class="titleV" x="1090" y="555" fill="{BLUE}" transform="rotate(90 1090 555)">Physical</text>

  <!-- ===== SOCIAL pills ===== -->
  <!-- Right edges: SN=410, CP=460 -->
  <g id="social">
    <rect class="pill" x="190" y="175" width="220" height="40" fill="{PINK}"/>
    <text class="label" x="300" y="201" text-anchor="middle">Social Networks</text>

    <rect class="pill" x="180" y="240" width="280" height="40" fill="{PINK}"/>
    <text class="label" x="320" y="266" text-anchor="middle">Community participation</text>
  </g>

  <!-- ===== PSYCHOLOGICAL pills (raised by ~20px) ===== -->
  <!-- Right edges: ES=420, SA=420, Purpose=410, Downshift=420 -->
  <g id="psy">
    <rect class="pill" x="180" y="480" width="240" height="40" fill="{ORANGE}"/>
    <text class="label" x="300" y="506" text-anchor="middle">Emotional security</text>

    <rect class="pill" x="180" y="530" width="240" height="40" fill="{ORANGE}"/>
    <text class="label" x="300" y="556" text-anchor="middle">Sense of autonomy</text>

    <rect class="pill" x="200" y="580" width="210" height="40" fill="{ORANGE}"/>
    <text class="label" x="305" y="606" text-anchor="middle">Purpose</text>

    <rect class="pill" x="180" y="630" width="240" height="40" fill="{ORANGE}"/>
    <text class="label" x="300" y="656" text-anchor="middle">Downshift</text>
  </g>

  <!-- ===== ENVIRONMENTAL pills — raised ===== -->
  <!-- y: 120, 165, 210, 255, 300 (Safety inside the frame) -->
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

  <!-- ===== PHYSICAL pill ===== -->
  <g id="phys">
    <rect class="pill" x="700" y="575" width="320" height="44" fill="{BLUE}"/>
    <text class="label" x="860" y="602" text-anchor="middle">Physical activity &amp; active lifestyle</text>
  </g>

  <!-- ===== Dotted Social→Environmental meta-arc (as in the original) ===== -->
  <path d="M120,95 C410,30 820,30 1080,95"
        stroke="{PINK}" stroke-width="4" stroke-dasharray="6 8" fill="none"/>

  <!-- ===== ARROWS — tips stop on pill borders ===== -->
  <!-- Tip x-values: Social Networks 406, Community participation 456, Psych ≈420, Physical 704 -->

  <!-- ENV → Social Networks (5) -->
  <path d="M740,140 C615,125 480,135 406,195" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M750,185 C620,175 490,160 406,195" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M740,230 C615,220 490,175 406,195" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M750,275 C620,265 490,190 406,195" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M700,320 C600,305 490,210 406,195" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- ENV → Community participation (5) -->
  <path d="M740,140 C610,145 530,245 456,260" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M750,185 C620,190 535,255 456,260" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M740,230 C610,235 535,268 456,260" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M750,275 C620,280 535,280 456,260" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M700,320 C610,330 540,300 456,260" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- ENV → Psychological (3) to ES/SA/Downshift (right edges ≈ 420) -->
  <path d="M750,185 C710,230 525,445 420,500" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M740,230 C700,270 520,495 420,550" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M700,320 C665,365 510,610 420,650" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- Safety → Physical -->
  <path d="M820,320 C810,420 780,505 704,595" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- PSY → Community participation (3 upward) -->
  <path d="M300,500 C305,460 315,340 456,260" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>
  <path d="M300,550 C305,510 315,355 456,260" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>
  <path d="M305,600 C305,560 318,370 456,260" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>

  <!-- Downshift → Physical -->
  <path d="M300,650 C485,635 670,610 704,595" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>

  <!-- ===== NEW: Social → Psychological (pink, as in the original) ===== -->
  <!-- Social Networks → Emotional security -->
  <path d="M406,195 C420,260 410,430 420,480"
        stroke="{PINK}" stroke-width="5" fill="none" marker-end="url(#arrow-pink)"/>

  <!-- Community participation → Sense of autonomy -->
  <path d="M456,260 C460,320 440,470 420,530"
        stroke="{PINK}" stroke-width="5" fill="none" marker-end="url(#arrow-pink)"/>

  <!-- Community participation → Downshift (small curve) -->
  <path d="M456,260 C455,330 445,600 420,650"
        stroke="{PINK}" stroke-width="5" fill="none" marker-end="url(#arrow-pink)"/>
</svg>
"""

st.components.v1.html(svg, height=840, scrolling=False)

with st.expander("Notes / geometry"):
    st.markdown("""
- **Psychological pills raised** by ~20px: y = 480, 530, 580, 630.
- **Environmental pills raised** (120, 165, 210, 255, 300). **Safety** is inside the frame (right edge 940; frame right 1080).
- Added **pink Social→Psychological arrows** (SN→ES, CP→SA, CP→Downshift) and the **dotted Social→Environmental** arc.
- Arrow tips land on pill borders at: Social (406/456), Psychological (~420), Physical (704).  
  If your rendering shows a 1-px variance, nudge the last x value by ±2 for that arrow.
""")
