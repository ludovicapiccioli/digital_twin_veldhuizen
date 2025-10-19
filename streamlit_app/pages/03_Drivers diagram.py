# pages/03_Drivers diagram.py
import streamlit as st
st.set_page_config(page_title="Drivers Diagram", page_icon="🧩", layout="wide")

st.subheader("Drivers Diagram - Interrelations across QoL Dimensions")

PINK   = "#ff69b4"   # Social-origin / pink arrows
ORANGE = "#f39c12"   # Psychological frame/pills
GREEN  = "#27ae60"   # Environmental-origin / green arrows
BLUE   = "#3498db"   # Physical frame/pill

svg = f"""
<svg id="drivers-svg" viewBox="0 0 1140 820" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Drivers diagram">
  <defs>
    <!-- Smaller arrowheads (Option A), keep your orientations -->
    <marker id="arrow-green" viewBox="0 0 10 6"
            markerWidth="6.5" markerHeight="6.5"
            refX="8.3" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 z" fill="{GREEN}"/>
    </marker>
    <marker id="arrow-pink" viewBox="0 0 10 6"
            markerWidth="6.5" markerHeight="6.5"
            refX="8.3" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 z" fill="{PINK}"/>
    </marker>
    <marker id="arrow-pink-340" viewBox="0 0 10 6"
            markerWidth="6.5" markerHeight="6.5"
            refX="8.3" refY="3" orient="35" markerUnits="strokeWidth">
      <path d="M0,0 L10,3 L0,6 z" fill="{PINK}"/>
    </marker>

    <style><![CDATA[
      .frame {{ fill: none; stroke-width: 4; rx: 20; ry: 20; }}
      .label {{ font: 700 16px 'Inter','Segoe UI',system-ui,-apple-system,sans-serif; fill: #fff; }}
      .pill  {{ rx: 22; ry: 22; stroke: #fff; stroke-width: 3; }}
      .titleV {{ font: 800 22px 'Inter','Segoe UI',system-ui,-apple-system,sans-serif; }}

      /* --- Interactivity styles --- */
      .node {{ cursor: pointer; }}
      .edge {{ pointer-events: stroke; }} /* allow hover on lines */
      .dim-title {{ pointer-events: none; }}

      /* default opacity */
      .node .pill, .edge {{ opacity: 0.85; transition: opacity .15s ease, filter .15s ease, stroke-width .15s ease; }}
      .edge {{ stroke-linecap: round; }}

      /* on hover context: fade others */
      .faded {{ opacity: 0.15; filter: grayscale(40%); }}

      /* highlight: make vivid and a tad thicker */
      .highlight {{ opacity: 1; filter: none; }}
      .edge.highlight {{ stroke-width: 4.2; }}
      .node.highlight .pill {{ stroke-width: 4; }}

      /* dotted meta-arc keeps its dash but can highlight too */
      .dotted {{ stroke-dasharray: 6 8; }}

      /* Improve text hit area a bit */
      .node text {{ user-select: none; pointer-events: none; }}
    ]]></style>
  </defs>

  <!-- ===== Frames with vertical titles OUTSIDE ===== -->
  <rect class="frame" x="80"  y="90"  width="440" height="280" stroke="{PINK}"/>
  <text class="titleV dim-title" x="60"  y="230" fill="{PINK}" transform="rotate(-90 60 230)">SOCIAL</text>

  <rect class="frame" x="80"  y="410" width="440" height="280" stroke="{ORANGE}"/>
  <text class="titleV dim-title" x="60"  y="650" fill="{ORANGE}" transform="rotate(-90 60 650)">Psychological</text>

  <rect class="frame" x="640" y="70"  width="440" height="310" stroke="{GREEN}"/>
  <text class="titleV dim-title" x="1090" y="130" fill="{GREEN}" transform="rotate(90 1090 130)">ENVIRONMENTAL</text>

  <rect class="frame" x="640" y="400" width="440" height="310" stroke="{BLUE}"/>
  <text class="titleV dim-title" x="1090" y="555" fill="{BLUE}" transform="rotate(90 1090 555)">Physical</text>

  <!-- ===== Nodes (pills) with data-node ids ===== -->
  <!-- SOCIAL -->
  <g class="node" data-node="SN">
    <rect class="pill" x="190" y="175" width="220" height="40" fill="{PINK}"/>
    <text class="label" x="300" y="201" text-anchor="middle">Social Networks</text>
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
    <rect class="pill" x="700" y="575" width="320" height="44" fill="{BLUE}"/>
    <text class="label" x="860" y="602" text-anchor="middle">Physical activity &amp; active lifestyle</text>
  </g>

  <!-- ===== Meta dotted arc (treat as edge Social→Environmental) ===== -->
  <path id="A00_Social_to_Env_arc" class="edge dotted"
        data-from="SOCIAL" data-to="ENV"
        d="M120,85 C410,20 820,20 990,68"
        stroke="{PINK}" stroke-width="3" fill="none" marker-end="url(#arrow-pink)"/>

  <!-- ========= EDGES with data-from / data-to ========= -->
  <!-- Pink (Social-origin) -->
  <path id="A01" class="edge" data-from="SN" data-to="Purpose"
        d="M194,195 C60,190 115,560 200,590"
        stroke="{PINK}" stroke-width="3" fill="none" marker-end="url(#arrow-pink-340)"/>

  <path id="A02" class="edge" data-from="SN" data-to="ES"
        d="M194,195 C110,230 130,395 180,490"
        stroke="{PINK}" stroke-width="3" fill="none" marker-end="url(#arrow-pink)"/>

  <path id="A03" class="edge" data-from="SN" data-to="SA"
        d="M194,195 C90,210 120,440 180,540"
        stroke="{PINK}" stroke-width="3" fill="none" marker-end="url(#arrow-pink)"/>

  <path id="A04" class="edge" data-from="CP" data-to="Purpose"
        d="M456,260 C470,340 440,540 410,590"
        stroke="{PINK}" stroke-width="3" fill="none" marker-end="url(#arrow-pink)"/>

  <path id="A05" class="edge" data-from="CP" data-to="Downshift"
        d="M456,260 C490,390 450,610 420,640"
        stroke="{PINK}" stroke-width="3" fill="none" marker-end="url(#arrow-pink)"/>

  <path id="A06" class="edge" data-from="CP" data-to="PA"
        d="M456,260 C560,330 640,560 704,595"
        stroke="{PINK}" stroke-width="3" fill="none" marker-end="url(#arrow-pink)"/>

  <!-- Green (Environmental-origin) -->
  <path id="A07" class="edge" data-from="PS" data-to="SN"
        d="M740,140 C615,125 480,135 406,195"
        stroke="{GREEN}" stroke-width="3" fill="none" marker-end="url(#arrow-green)"/>

  <path id="A08" class="edge" data-from="PS" data-to="SA"
        d="M740,140 C690,180 520,470 420,520"
        stroke="{GREEN}" stroke-width="3" fill="none" marker-end="url(#arrow-green)"/>

  <path id="A09" class="edge" data-from="GS" data-to="CP"
        d="M750,185 C620,190 535,255 456,260"
        stroke="{GREEN}" stroke-width="3" fill="none" marker-end="url(#arrow-green)"/>

  <path id="A10" class="edge" data-from="GS" data-to="Downshift"
        d="M750,185 C680,240 520,575 420,640"
        stroke="{GREEN}" stroke-width="3" fill="none" marker-end="url(#arrow-green)"/>

  <path id="A11" class="edge" data-from="MA" data-to="CP"
        d="M740,230 C610,235 535,268 456,260"
        stroke="{GREEN}" stroke-width="3" fill="none" marker-end="url(#arrow-green)"/>

  <path id="A12" class="edge" data-from="SI" data-to="SN"
        d="M750,275 C620,265 490,190 406,195"
        stroke="{GREEN}" stroke-width="3" fill="none" marker-end="url(#arrow-green)"/>

  <path id="A13" class="edge" data-from="SI" data-to="CP"
        d="M750,275 C620,280 535,280 456,260"
        stroke="{GREEN}" stroke-width="3" fill="none" marker-end="url(#arrow-green)"/>

  <path id="A14" class="edge" data-from="Safety" data-to="CP"
        d="M700,320 C610,330 540,300 456,260"
        stroke="{GREEN}" stroke-width="3" fill="none" marker-end="url(#arrow-green)"/>

  <path id="A15" class="edge" data-from="Safety" data-to="Downshift"
        d="M700,320 C640,380 510,600 420,640"
        stroke="{GREEN}" stroke-width="3" fill="none" marker-end="url(#arrow-green)"/>

  <path id="A16" class="edge" data-from="ENV" data-to="PA"
        d="M860,380 C835,450 795,520 760,575"
        stroke="{GREEN}" stroke-width="3" fill="none" marker-end="url(#arrow-green)"/>

  <!-- ====== Interactivity script ====== -->
  <script><![CDATA[
    (function () {{
      const svg = document.getElementById('drivers-svg');
      const nodes = Array.from(svg.querySelectorAll('.node'));
      const edges = Array.from(svg.querySelectorAll('.edge'));

      // Build adjacency maps
      const outgoing = {{}};
      const incoming = {{}};

      edges.forEach(e => {{
        const from = e.getAttribute('data-from');
        const to   = e.getAttribute('data-to');
        if (!from || !to) return;
        (outgoing[from] = outgoing[from] || []).push(e);
        (incoming[to]   = incoming[to]   || []).push(e);
      }});

      function clearAll() {{
        nodes.forEach(n => n.classList.remove('highlight', 'faded'));
        edges.forEach(e => e.classList.remove('highlight', 'faded'));
      }}

      function fadeAll() {{
        nodes.forEach(n => n.classList.add('faded'));
        edges.forEach(e => e.classList.add('faded'));
      }}

      function highlightNode(nodeId) {{
        fadeAll();
        // highlight the node itself
        const me = svg.querySelector(`.node[data-node="${{nodeId}}"]`);
        if (me) me.classList.add('highlight');

        // outgoing edges + their targets
        (outgoing[nodeId] || []).forEach(e => {{
          e.classList.add('highlight');
          const tgt = e.getAttribute('data-to');
          const n   = svg.querySelector(`.node[data-node="${{tgt}}"]`);
          if (n) n.classList.add('highlight');
        }});

        // incoming edges + their sources
        (incoming[nodeId] || []).forEach(e => {{
          e.classList.add('highlight');
          const src = e.getAttribute('data-from');
          const n   = svg.querySelector(`.node[data-node="${{src}}"]`);
          if (n) n.classList.add('highlight');
        }});
      }}

      // Hover on nodes
      nodes.forEach(n => {{
        const id = n.getAttribute('data-node');
        n.addEventListener('mouseenter', () => highlightNode(id));
        n.addEventListener('mouseleave', clearAll);

        // Tap/click toggle for touch users
        n.addEventListener('click', (ev) => {{
          ev.stopPropagation();
          const active = n.classList.contains('highlight');
          clearAll();
          if (!active) highlightNode(id);
        }});
      }});

      // Hover on edges (highlight edge + its endpoints)
      edges.forEach(e => {{
        e.addEventListener('mouseenter', () => {{
          fadeAll();
          e.classList.add('highlight');
          const from = e.getAttribute('data-from');
          const to   = e.getAttribute('data-to');
          const nf   = svg.querySelector(`.node[data-node="${{from}}"]`);
          const nt   = svg.querySelector(`.node[data-node="${{to}}"]`);
          if (nf) nf.classList.add('highlight');
          if (nt) nt.classList.add('highlight');
        }});
        e.addEventListener('mouseleave', clearAll);

        e.addEventListener('click', (ev) => {{
          ev.stopPropagation();
          const isOn = e.classList.contains('highlight');
          clearAll();
          if (!isOn) {{
            e.classList.add('highlight');
            const from = e.getAttribute('data-from');
            const to   = e.getAttribute('data-to');
            const nf   = svg.querySelector(`.node[data-node="${{from}}"]`);
            const nt   = svg.querySelector(`.node[data-node="${{to}}"]`);
            if (nf) nf.classList.add('highlight');
            if (nt) nt.classList.add('highlight');
          }}
        }});
      }});

      // Click on empty canvas clears
      svg.addEventListener('click', clearAll);
    }})();
  ]]></script>
</svg>
"""

st.components.v1.html(svg, height=860, scrolling=False)







