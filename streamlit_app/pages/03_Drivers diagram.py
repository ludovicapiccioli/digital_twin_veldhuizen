# pages/03_Drivers diagram.py
import streamlit as st
st.set_page_config(page_title="Drivers Diagram", page_icon="🧩", layout="wide")

st.title("Drivers Diagram — Interrelations across Dimensions")
st.caption("Vertical titles outside frames. Environmental pills raised. Arrow tips stop at pill edges (no text overlap).")

PINK   = "#ff69b4"   # Social
ORANGE = "#f39c12"   # Psychological
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
    <style><![CDATA[
      .frame {{ fill: none; stroke-width: 4; rx: 20; ry: 20; }}
      .label {{ font: 700 16px 'Inter','Segoe UI',system-ui,-apple-system,sans-serif; fill: #fff; }}
      .pill  {{ rx: 22; ry: 22; stroke: #fff; stroke-width: 3; }}
      .titleV {{ font: 800 22px 'Inter','Segoe UI',system-ui,-apple-system,sans-serif; }}
    ]]></style>
  </defs>

  <!-- ===== Frames (titles OUTSIDE and vertical) ===== -->
  <!-- Frame geometry (x,y,w,h) -->
  <!-- Social -->
  <rect class="frame" x="80"  y="90"  width="440" height="280" stroke="{PINK}"/>
  <text class="titleV" x="60" y="230" fill="{PINK}" transform="rotate(-90 60 230)">SOCIAL</text>

  <!-- Psychological -->
  <rect class="frame" x="80"  y="410" width="440" height="280" stroke="{ORANGE}"/>
  <text class="titleV" x="60" y="550" fill="{ORANGE}" transform="rotate(-90 60 550)">Psychological</text>

  <!-- Environmental (made a bit taller to match the source look) -->
  <rect class="frame" x="640" y="70"  width="440" height="310" stroke="{GREEN}"/>
  <text class="titleV" x="1090" y="225" fill="{GREEN}" transform="rotate(90 1090 225)">ENVIRONMENTAL</text>

  <!-- Physical -->
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

  <!-- ===== PSYCHOLOGICAL pills ===== -->
  <!-- Right edges: ES=420, SA=420, Purpose=410, Downshift=420 -->
  <g id="psy">
    <rect class="pill" x="180" y="500" width="240" height="40" fill="{ORANGE}"/>
    <text class="label" x="300" y="526" text-anchor="middle">Emotional security</text>

    <rect class="pill" x="180" y="550" width="240" height="40" fill="{ORANGE}"/>
    <text class="label" x="300" y="576" text-anchor="middle">Sense of autonomy</text>

    <rect class="pill" x="200" y="600" width="210" height="40" fill="{ORANGE}"/>
    <text class="label" x="305" y="626" text-anchor="middle">Purpose</text>

    <rect class="pill" x="180" y="650" width="240" height="40" fill="{ORANGE}"/>
    <text class="label" x="300" y="676" text-anchor="middle">Downshift</text>
  </g>

  <!-- ===== ENVIRONMENTAL pills — raised upwards ===== -->
  <!-- All pills moved ~30px up; Safety firmly inside the frame -->
  <!-- Proximity y=120, Green y=165, Mobility y=210, SocialInfra y=255, Safety y=300 -->
  <g id="env">
    <rect class="pill" x="740" y="120" width="300" height="40" fill="{GREEN}"/>
    <text class="label" x="890" y="146" text-anchor="middle">Proximity to services</text>

    <rect class="pill" x="750" y="165" width="280" height="40" fill="{GREEN}"/>
    <text class="label" x="890" y="191" text-anchor="middle">Green spaces</text>

    <rect class="pill" x="740" y="210" width="300" height="40" fill="{GREEN}"/>
    <text class="label" x="890" y="236" text-anchor="middle">Mobility &amp; Accessibility</text>

    <rect class="pill" x="750" y="255" width="280" height="40" fill="{GREEN}"/>
    <text class="label" x="890" y="281" text-anchor="middle">Social infrastructures</text>

    <!-- SAFETY moved up & left; right edge = 940, inside frame right (=1080), bottom = 340 < 380 -->
    <rect class="pill" x="700" y="300" width="240" height="40" fill="{GREEN}"/>
    <text class="label" x="820" y="326" text-anchor="middle">Safety</text>
  </g>

  <!-- ===== PHYSICAL pill ===== -->
  <!-- Left edge x=700; arrow tips target ≈ 704 -->
  <g id="phys">
    <rect class="pill" x="700" y="575" width="320" height="44" fill="{BLUE}"/>
    <text class="label" x="860" y="602" text-anchor="middle">Physical activity &amp; active lifestyle</text>
  </g>

  <!-- ===== ARROWS — tips stop on pill borders ===== -->
  <!-- Tip x-values: SN=406, CP=456, Psych≈420, Physical=704 -->

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
  <path d="M750,185 C710,230 525,445 420,520" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M740,230 C700,270 520,495 420,570" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M700,320 C665,365 510,610 420,670" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- Safety → Physical (tip at blue pill left edge ≈ 704) -->
  <path d="M820,320 C810,420 780,505 704,595" stroke="{GREEN}" stroke-width="5" fill="none" marker-end="url(#arrow-green)"/>

  <!-- PSY → Community participation (3 upward) -->
  <path d="M300,520 C305,480 315,350 456,260" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>
  <path d="M300,570 C305,530 315,365 456,260" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>
  <path d="M305,620 C305,580 318,375 456,260" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>

  <!-- Downshift → Physical (tip at 704) -->
  <path d="M300,670 C485,655 670,630 704,595" stroke="{ORANGE}" stroke-width="5" fill="none" marker-end="url(#arrow-orange)"/>
</svg>
"""

st.components.v1.html(svg, height=840, scrolling=False)

with st.expander("Notes / precise geometry"):
    st.markdown("""
- **Frames**: Social (80,90,440,280), Psych (80,410,440,280), Environmental (640,70,440,310), Physical (640,400,440,310).
- **Vertical titles**: outside frames—rotated **−90°** on the left and **+90°** on the right to mirror your reference.
- **Environmental pills raised**: y = 120, 165, 210, 255, 300. **Safety** is now well inside (right edge 940; frame right 1080).
- **Arrow tips** hit pill borders at exact x’s: Social Networks **406**, Community participation **456**, Psychological **~420**, Physical **704**.
  Adjust by ±2 if rendering shows a 1-px variance on your screen.
""")
