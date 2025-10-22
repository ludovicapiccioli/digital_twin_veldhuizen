# pages/03_Drivers diagram.py
import streamlit as st
st.set_page_config(page_title="Drivers Diagram", page_icon="🧩", layout="wide")

st.subheader("Drivers Diagram - Nodes only (no arrows)")

PINK   = "#ff69b4"   # Social
ORANGE = "#f39c12"   # Psychological
GREEN  = "#27ae60"   # Environmental
PHYSICAL = "#B39DDB" # Physical
LIGHTBLUE = "#1E88E5"

svg = f"""
<svg id="drivers-svg" viewBox="0 0 1140 820" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Drivers diagram (nodes only)">
  <defs>
    <style><![CDATA[
      .frame {{ fill: none; stroke-width: 4; rx: 20; ry: 20; }}
      .label {{ font: 700 16px 'Inter','Segoe UI',system-ui,-apple-system,sans-serif; fill: #fff; }}
      .pill  {{ rx: 22; ry: 22; stroke: #fff; stroke-width: 3; }}
      .titleV {{ font: 800 22px 'Inter','Segoe UI',system-ui,-apple-system,sans-serif; }}

      .node[data-node="Purpose"] .label,
      .node[data-node="Downshift"] .label,
      .node[data-node="CP"] .label,
      .node[data-node="PA"] .label {{ fill: {LIGHTBLUE}; }}

      .node {{ cursor: pointer; }}
      .faded {{ opacity: 0.15; filter: grayscale(40%); }}
      .highlight {{ opacity: 1; filter: none; }}
      .node.highlight .pill {{ stroke-width: 4; }}
      .node text {{ user-select: none; pointer-events: none; }}
    ]]></style>
  </defs>

  <!-- Frames -->
  <rect class="frame" x="80"  y="90"  width="440" height="280" stroke="{PINK}"/>
  <text class="titleV" x="60"  y="230" fill="{PINK}" transform="rotate(-90 60 230)">SOCIAL</text>

  <rect class="frame" x="80"  y="410" width="440" height="280" stroke="{ORANGE}"/>
  <text class="titleV" x="60"  y="650" fill="{ORANGE}" transform="rotate(-90 60 650)">Psychological</text>

  <rect class="frame" x="640" y="70"  width="440" height="310" stroke="{GREEN}"/>
  <text class="titleV" x="1090" y="130" fill="{GREEN}" transform="rotate(90 1090 130)">ENVIRONMENTAL</text>

  <rect class="frame" x="640" y="400" width="440" height="310" stroke="{PHYSICAL}"/>
  <text class="titleV" x="1090" y="555" fill="{PHYSICAL}" transform="rotate(90 1090 555)">Physical</text>

  <!-- Nodes -->
  <!-- SOCIAL -->
  <g class="node" data-node="SN">
    <rect class="pill" x="190" y="175" width="220" height="40" fill="{PINK}"/>
    <text class="label" x="300" y="201" text-anchor="middle">Social networks</text>
  </g>

  <g class="node" data-node="CP">
    <rect class="pill" x="180" y="240" width="280" height="40" fill="{PINK}"/>
    <text class="label" x="320" y="266" text-anchor="middle">Community participation</text>
  </g>

  <!-- PSYCHOLOGICAL -->
  <g class="node" data-node="ES">
    <rect class="pill" x="180" y="470" width="240" height="40" fill="{ORANGE}"/>
    <text class="label" x="300" y="496" text-anchor="middle">Emotional security</text>
  </g>

  <g class="node" data-node="SA">
    <rect class="pill" x="180" y="520" width="240" height="40" fill="{ORANGE}"/>
    <text class="label" x="300" y="546" text-anchor="middle">Sense of autonomy</text>
  </g>

  <g class="node" data-node="Purpose">
    <rect class="pill" x="200" y="570" width="210" height="40" fill="{ORANGE}"/>
    <text class="label" x="305" y="596" text-anchor="middle">Purpose</text>
  </g>

  <g class="node" data-node="Downshift">
    <rect class="pill" x="180" y="620" width="240" height="40" fill="{ORANGE}"/>
    <text class="label" x="300" y="646" text-anchor="middle">Downshift</text>
  </g>

  <!-- ENVIRONMENTAL -->
  <g class="node" data-node="PS">
    <rect class="pill" x="740" y="120" width="300" height="40" fill="{GREEN}"/>
    <text class="label" x="890" y="146" text-anchor="middle">Proximity to services</text>
  </g>

  <g class="node" data-node="GS">
    <rect class="pill" x="750" y="165" width="280" height="40" fill="{GREEN}"/>
    <text class="label" x="890" y="191" text-anchor="middle">Green spaces</text>
  </g>

  <g class="node" data-node="MA">
    <rect class="pill" x="740" y="210" width="300" height="40" fill="{GREEN}"/>
    <text class="label" x="890" y="236" text-anchor="middle">Mobility &amp; Accessibility</text>
  </g>

  <g class="node" data-node="SI">
    <rect class="pill" x="750" y="255" width="280" height="40" fill="{GREEN}"/>
    <text class="label" x="890" y="281" text-anchor="middle">Social infrastructures</text>
  </g>

  <g class="node" data-node="Safety">
    <rect class="pill" x="700" y="300" width="240" height="40" fill="{GREEN}"/>
    <text class="label" x="820" y="326" text-anchor="middle">Safety</text>
  </g>

  <!-- PHYSICAL -->
  <g class="node" data-node="PA">
    <rect class="pill" x="700" y="575" width="320" height="44" fill="{PHYSICAL}"/>
    <text class="label" x="860" y="602" text-anchor="middle">Physical activity &amp; active lifestyle</text>
  </g>

  <script><![CDATA[
    (function () {{
      const svg = document.getElementById('drivers-svg');
      const nodes = Array.from(svg.querySelectorAll('.node'));

      function clearAll() {{
        nodes.forEach(n => n.classList.remove('highlight', 'faded'));
      }}
      function fadeAll() {{
        nodes.forEach(n => n.classList.add('faded'));
      }}
      function highlightNode(nodeId) {{
        fadeAll();
        const me = svg.querySelector(`.node[data-node="${{nodeId}}"]`);
        if (me) me.classList.add('highlight');
      }}

      nodes.forEach(n => {{
        const id = n.getAttribute('data-node');
        n.addEventListener('mouseenter', () => highlightNode(id));
        n.addEventListener('mouseleave', clearAll);
        n.addEventListener('click', (ev) => {{
          ev.stopPropagation();
          const active = n.classList.contains('highlight');
          clearAll();
          if (!active) highlightNode(id);
        }});
      }});
      svg.addEventListener('click', clearAll);
    }})()
  ]]></script>
</svg>
"""

st.components.v1.html(svg, height=860, scrolling=False)
