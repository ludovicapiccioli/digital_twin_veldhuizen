# pages/03_Drivers diagram.py
import streamlit as st
from textwrap import dedent

st.set_page_config(page_title="Drivers Diagram", page_icon="🧩", layout="wide")
st.title("Drivers Diagram — Interrelations across Dimensions")
st.caption("Static SVG replica of the report figure (precise layout, colors, curves).")

# Colors
PINK = "#ff69b4"         # Social frame + nodes
ORANGE = "#f39c12"       # Psychological
GREEN = "#27ae60"        # Environmental
BLUE = "#3498db"         # Physical
TEXT = "#5b6770"
BG = "#ffffff"

# SVG (1000x700 canvas). Tweak positions if you want millimetre-perfect changes.
svg = f"""
<svg viewBox="0 0 1000 700" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Drivers diagram">
  <defs>
    <!-- Arrowheads by source dimension -->
    <marker id="arrow-green" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 z" fill="{GREEN}"/>
    </marker>
    <marker id="arrow-orange" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 z" fill="{ORANGE}"/>
    </marker>

    <!-- Common styles -->
    <style><![CDATA[
      .frame {{ fill: none; stroke-width: 3; rx: 14; ry: 14; }}
      .label   {{ font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif; font-weight: 700; font-size: 20px; }}
      .sublabel{{ font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif; font-weight: 600; font-size: 16px; fill: {TEXT}; }}
      .pill-text {{ font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif; font-weight: 600; font-size: 16px; fill: #ffffff; }}
      .pill {{ rx: 18; ry: 18; }}
      .node-dot {{ stroke: #ffffff; stroke-width: 3; }}
    ]]></style>
  </defs>

  <!-- Frames -->
  <rect class="frame" x="80"  y="60"  width="360" height="260" stroke="{PINK}"/>
  <text x="110" y="95" class="label" fill="{PINK}">SOCIAL</text>

  <rect class="frame" x="80"  y="380" width="360" height="260" stroke="{ORANGE}"/>
  <text x="110" y="415" class="label" fill="{ORANGE}">Psychological</text>

  <rect class="frame" x="560" y="60"  width="360" height="260" stroke="{GREEN}"/>
  <text x="590" y="95" class="label" fill="{GREEN}">ENVIRONMENTAL</text>

  <rect class="frame" x="560" y="380" width="360" height="260" stroke="{BLUE}"/>
  <text x="590" y="415" class="label" fill="{BLUE}">Physical</text>

  <!-- SOCIAL nodes (pills) -->
  <g id="social-nodes">
    <circle cx="280" cy="170" r="14" fill="{PINK}" class="node-dot"/>
    <text x="140" y="170" class="sublabel">Social Networks</text>

    <circle cx="260" cy="235" r="14" fill="{PINK}" class="node-dot"/>
    <text x="100" y="235" class="sublabel">Community participation</text>
  </g>

  <!-- PSYCHOLOGICAL nodes -->
  <g id="psy-nodes">
    <circle cx="240" cy="470" r="14" fill="{ORANGE}" class="node-dot"/>
    <text x="140" y="470" class="sublabel">Emotional security</text>

    <circle cx="240" cy="510" r="14" fill="{ORANGE}" class="node-dot"/>
    <text x="140" y="510" class="sublabel">Sense of autonomy</text>

    <circle cx="240" cy="550" r="14" fill="{ORANGE}" class="node-dot"/>
    <text x="190" y="550" class="sublabel">Purpose</text>

    <circle cx="240" cy="610" r="14" fill="{ORANGE}" class="node-dot"/>
    <text x="170" y="610" class="sublabel">Downshift</text>
  </g>

  <!-- ENVIRONMENTAL nodes -->
  <g id="env-nodes">
    <circle cx="860" cy="155" r="14" fill="{GREEN}" class="node-dot"/>
    <text x="680" y="155" class="sublabel">Proximity to services</text>

    <circle cx="860" cy="195" r="14" fill="{GREEN}" class="node-dot"/>
    <text x="740" y="195" class="sublabel">Green spaces</text>

    <circle cx="860" cy="235" r="14" fill="{GREEN}" class="node-dot"/>
    <text x="710" y="235" class="sublabel">Mobility &amp; Accessibility</text>

    <circle cx="860" cy="275" r="14" fill="{GREEN}" class="node-dot"/>
    <text x="720" y="275" class="sublabel">Social infrastructures</text>

    <circle cx="860" cy="315" r="14" fill="{GREEN}" class="node-dot"/>
    <text x="805" y="315" class="sublabel">Safety</text>
  </g>

  <!-- PHYSICAL node -->
  <g id="phy-nodes">
    <circle cx="820" cy="560" r="16" fill="{BLUE}" class="node-dot"/>
    <text x="620" y="560" class="sublabel">Physical activity &amp; active lifestyle</text>
  </g>

  <!-- Curved arrows from ENVIRONMENTAL (green) -->
  <!-- Use smooth cubic Beziers to mimic the reference curves -->
  <path d="M860,155 C760,135 460,150 294,166" stroke="{GREEN}" stroke-width="4" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M860,195 C760,185 450,200 274,228" stroke="{GREEN}" stroke-width="4" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M860,235 C760,235 460,240 274,234" stroke="{GREEN}" stroke-width="4" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M860,275 C760,285 470,270 274,240" stroke="{GREEN}" stroke-width="4" fill="none" marker-end="url(#arrow-green)"/>
  <path d="M860,315 C760,335 460,300 260,245" stroke="{GREEN}" stroke-width="4" fill="none" marker-end="url(#arrow-green)"/>

  <!-- Green vertical to Physical -->
  <path d="M860,315 C860,420 840,520 822,546" stroke="{GREEN}" stroke-width="4" fill="none" marker-end="url(#arrow-green)"/>

  <!-- Curved arrows from PSYCHOLOGICAL (orange) -->
  <path d="M240,470 C240,440 248,300 258,248" stroke="{ORANGE}" stroke-width="4" fill="none" marker-end="url(#arrow-orange)"/>
  <path d="M240,510 C240,480 248,305 258,248" stroke="{ORANGE}" stroke-width="4" fill="none" marker-end="url(#arrow-orange)"/>
  <path d="M240,550 C240,520 248,308 258,248" stroke="{ORANGE}" stroke-width="4" fill="none" marker-end="url(#arrow-orange)"/>
  <path d="M240,610 C420,600 640,590 802,558" stroke="{ORANGE}" stroke-width="4" fill="none" marker-end="url(#arrow-orange)"/>

  <!-- Light dotted Social-to-Environmental arc (optional, as in some versions) -->
  <!-- <path d="M300,140 C420,60 740,60 860,140" stroke="{PINK}" stroke-width="3" fill="none" stroke-dasharray="4 6"/> -->
</svg>
"""

# Render the SVG
st.components.v1.html(svg, height=720, scrolling=False)

with st.expander("Notes"):
    st.markdown("""
- This is a **static SVG** so the visuals match your report precisely (rounded frames, node dots, smooth curved arrows, tidy arrowheads).
- If you want hover effects (e.g., highlight edges of a node), we can add a tiny bit of JavaScript to the SVG, still with `st.components.v1.html` and **no extra dependencies**.
- To tweak positions or curves: edit the `cx, cy` of circles and the `C` control points in the `<path>` commands.
""")
