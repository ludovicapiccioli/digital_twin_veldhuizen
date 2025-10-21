import streamlit as st

st.set_page_config(layout="wide", page_title="Intervention Diagram")

svg = r'''
<svg viewBox="0 0 960 560" xmlns="http://www.w3.org/2000/svg"
     style="width:100%;height:auto;display:block;background:none;">  <!-- transparent -->

  <!-- defs -->
  <defs>
    <marker id="arrowGreen" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,5 L0,10 z" fill="#19a974"/>
    </marker>
    <marker id="arrowRed" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,5 L0,10 z" fill="#e85959"/>
    </marker>
    <filter id="soft" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.15"/>
    </filter>
    <style>
      .cap { font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial; font-weight:600; }
      .tiny { font-size:12px; fill:#666; }
      .pill { font-size:14px; font-weight:600; fill:#fff; }
      .score { font-size:36px; font-weight:800; fill:#fff; }
      .mult { font-size:16px; font-weight:700; }
    </style>
  </defs>

  <!-- Left: Intervention -->
  <g transform="translate(40,180)">
    <rect x="0" y="0" rx="20" ry="20" width="200" height="130" fill="#fff" stroke="#111" stroke-width="3" filter="url(#soft)"/>
    <text x="100" y="-18" text-anchor="middle" class="cap" fill="#111" font-size="16">Intervention</text>
    <rect x="20" y="25" rx="20" ry="20" width="160" height="80" fill="#000"/>
    <text x="100" y="75" text-anchor="middle" class="pill">Benches</text>
    <g transform="translate(-8,35)">
      <circle cx="20" cy="30" r="22" fill="#bdbdbd"/>
      <text x="20" y="35" text-anchor="middle" class="cap" font-size="16" fill="#fff">+3</text>
    </g>
  </g>

  <!-- Nodes with WHITE bubbles (outer rects) -->
  <!-- Social -->
  <g transform="translate(420,20)">
    <text x="160" y="20" class="cap" fill="#ff80bf" font-size="16" text-anchor="middle">SOCIAL DIMENSION</text>
    <rect x="0" y="30" rx="22" ry="22" width="320" height="90" fill="#ffffff" stroke="#ff80bf" stroke-width="4" filter="url(#soft)"/>
    <rect x="30" y="48" rx="18" ry="18" width="260" height="54" fill="#ff9ad5"/>
    <text x="160" y="82" text-anchor="middle" class="pill">Social networks</text>
  </g>

  <!-- Physical -->
  <g transform="translate(420,170)">
    <text x="120" y="10" class="cap" fill="#d90429" font-size="16">Physical dimension</text>
    <rect x="0" y="20" rx="22" ry="22" width="240" height="90" fill="#ffffff" stroke="#d90429" stroke-width="4" filter="url(#soft)"/>
    <rect x="20" y="38" rx="18" ry="18" width="200" height="54" fill="#b60021"/>
    <text x="120" y="72" text-anchor="middle" class="pill">Physical activity</text>
  </g>

  <!-- Environmental -->
  <g transform="translate(420,300)">
    <text x="120" y="10" class="cap" fill="#00b894" font-size="16">ENVIRONMENTAL DIMENSION</text>
    <rect x="0" y="20" rx="22" ry="22" width="260" height="90" fill="#ffffff" stroke="#00b894" stroke-width="4" filter="url(#soft)"/>
    <rect x="30" y="38" rx="18" ry="18" width="200" height="54" fill="#00c853"/>
    <text x="130" y="72" text-anchor="middle" class="pill">Safety</text>
  </g>

  <!-- Psychological -->
  <g transform="translate(420,430)">
    <text x="150" y="10" class="cap" fill="#ff9800" font-size="16">Psychological dimension</text>
    <rect x="0" y="20" rx="22" ry="22" width="300" height="90" fill="#ffffff" stroke="#ff9800" stroke-width="4" filter="url(#soft)"/>
    <rect x="30" y="38" rx="18" ry="18" width="240" height="54" fill="#ff8f2d"/>
    <text x="150" y="72" text-anchor="middle" class="pill">Downshift</text>
  </g>

  <!-- Right: Quality of Life (top card already white) -->
  <g transform="translate(770,160)">
    <text x="100" y="-18" class="cap" fill="#5f9ea0" font-size="18" text-anchor="middle">QUALITY OF LIFE</text>
    <rect x="0" y="0" rx="26" ry="26" width="180" height="238" fill="#ffffff" stroke="#6fa28e" stroke-width="3" filter="url(#soft)"/>
    <g transform="translate(0,128)">
      <rect x="0" y="0" rx="26" ry="26" width="180" height="110" fill="#5f8f75"/>
      <text x="90" y="70" text-anchor="middle" class="score">+12</text>
    </g>
    <g transform="translate(14,26)">
      <text class="tiny" x="0" y="0">+12 from Social</text>
      <text class="tiny" x="0" y="18">+3 from Physical</text>
      <text class="tiny" x="0" y="36">-6 from Environmental</text>
      <text class="tiny" x="0" y="54">+3 from Psychological</text>
    </g>
  </g>

  <!-- Node badges -->
  <g>
    <g transform="translate(740,78)">
      <circle cx="0" cy="0" r="16" fill="#bdbdbd"/><text x="0" y="5" text-anchor="middle" class="cap" font-size="13" fill="#fff">+6</text>
    </g>
    <g transform="translate(670,240)">
      <circle cx="0" cy="0" r="16" fill="#bdbdbd"/><text x="0" y="5" text-anchor="middle" class="cap" font-size="13" fill="#fff">+3</text>
    </g>
    <g transform="translate(660,372)">
      <circle cx="0" cy="0" r="16" fill="#bdbdbd"/><text x="0" y="5" text-anchor="middle" class="cap" font-size="13" fill="#fff">-3</text>
    </g>
    <g transform="translate(620,520)">
      <circle cx="0" cy="0" r="16" fill="#bdbdbd"/><text x="0" y="5" text-anchor="middle" class="cap" font-size="13" fill="#fff">+3</text>
    </g>
  </g>

  <!-- Arrows & multipliers (unchanged sizing/positions from last tweak) -->
  <path d="M240,245 C350,140 370,110 440,90" fill="none" stroke="#19a974" stroke-width="7" marker-end="url(#arrowGreen)"/>
  <text x="360" y="150" class="cap mult" fill="#19a974">x2</text>

  <path d="M240,245 C330,235 350,230 420,240" fill="none" stroke="#19a974" stroke-width="5" marker-end="url(#arrowGreen)"/>
  <text x="346" y="232" class="cap mult" fill="#19a974">x1</text>

  <path d="M240,245 C320,300 350,315 420,330" fill="none" stroke="#e85959" stroke-width="5" marker-end="url(#arrowRed)"/>
  <text x="342" y="302" class="cap mult" fill="#e85959">x-1</text>

  <path d="M240,245 C320,360 360,400 420,460" fill="none" stroke="#19a974" stroke-width="5" marker-end="url(#arrowGreen)"/>
  <text x="352" y="382" class="cap mult" fill="#19a974">x1</text>

  <path d="M740,90 C800,140 820,220 860,280" fill="none" stroke="#19a974" stroke-width="7" marker-end="url(#arrowGreen)"/>
  <text x="835" y="165" class="cap mult" fill="#19a974">x2</text>

  <path d="M660,230 C740,230 760,250 860,280" fill="none" stroke="#19a974" stroke-width="5" marker-end="url(#arrowGreen)"/>
  <text x="798" y="248" class="cap mult" fill="#19a974">x1</text>

  <path d="M680,360 C760,340 780,320 860,300" fill="none" stroke="#19a974" stroke-width="7" marker-end="url(#arrowGreen)"/>
  <text x="795" y="330" class="cap mult" fill="#19a974">x2</text>

  <path d="M720,480 C780,440 800,420 860,360" fill="none" stroke="#19a974" stroke-width="5" marker-end="url(#arrowGreen)"/>
  <text x="808" y="420" class="cap mult" fill="#19a974">x1</text>

</svg>
'''

st.components.v1.html(svg, height=640, scrolling=False)
