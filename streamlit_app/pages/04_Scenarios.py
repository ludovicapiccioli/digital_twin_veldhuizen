import streamlit as st

st.set_page_config(layout="wide", page_title="Intervention Diagram")

# Inline SVG so the diagram renders exactly and consistently in Streamlit
svg = r'''
<svg width="960" height="560" viewBox="0 0 960 560" xmlns="http://www.w3.org/2000/svg" style="background:#f2f2f2;">

  <!-- ========== defs ========== -->
  <defs>
    <marker id="arrowGreen" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
      <path d="M0,0 L12,6 L0,12 z" fill="#19a974"/>
    </marker>
    <marker id="arrowRed" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
      <path d="M0,0 L12,6 L0,12 z" fill="#e85959"/>
    </marker>
    <filter id="soft" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.15"/>
    </filter>
    <style>
      .cap { font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial; font-weight:600; }
      .text { font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial; }
      .tiny { font-size:12px; fill:#666; }
      .label { font-size:16px; font-weight:700; fill:#111; }
      .pill { font-size:14px; font-weight:600; fill:#fff; }
      .score { font-size:36px; font-weight:800; fill:#fff; }
      .sub { font-size:14px; fill:#2e7d32; font-weight:700; }
    </style>
  </defs>

  <!-- ========== Left: Intervention ========== -->
  <g transform="translate(40,180)">
    <rect x="0" y="0" rx="20" ry="20" width="200" height="130" fill="#fff" stroke="#111" stroke-width="3" filter="url(#soft)"/>
    <text x="100" y="-18" text-anchor="middle" class="cap" fill="#111" font-size="16">Intervention</text>
    <rect x="20" y="25" rx="20" ry="20" width="160" height="80" fill="#000"/>
    <text x="100" y="75" text-anchor="middle" class="pill">Benches</text>

    <!-- small +3 badge -->
    <g transform="translate(-8,35)">
      <circle cx="20" cy="30" r="22" fill="#bdbdbd"/>
      <text x="20" y="35" text-anchor="middle" class="cap" font-size="16" fill="#fff">+3</text>
    </g>
  </g>

  <!-- Node helpers -->
  <!-- Social -->
  <g transform="translate(420,20)">
    <text x="160" y="20" class="cap" fill="#ff80bf" font-size="16">SOCIAL DIMENSION</text>
    <rect x="0" y="30" rx="22" ry="22" width="320" height="90" fill="#ffd6eb" stroke="#ff80bf" stroke-width="4" filter="url(#soft)"/>
    <rect x="30" y="48" rx="18" ry="18" width="260" height="54" fill="#ff9ad5"/>
    <text x="160" y="82" text-anchor="middle" class="pill">Social networks</text>
  </g>

  <!-- Physical -->
  <g transform="translate(420,170)">
    <text x="120" y="10" class="cap" fill="#d90429" font-size="16">Physical dimension</text>
    <rect x="0" y="20" rx="22" ry="22" width="240" height="90" fill="#ffd6d6" stroke="#d90429" stroke-width="4" filter="url(#soft)"/>
    <rect x="20" y="38" rx="18" ry="18" width="200" height="54" fill="#b60021"/>
    <text x="120" y="72" text-anchor="middle" class="pill">Physical activity</text>
  </g>

  <!-- Environmental -->
  <g transform="translate(420,300)">
    <text x="120" y="10" class="cap" fill="#00b894" font-size="16">ENVIRONMENTAL DIMENSION</text>
    <rect x="0" y="20" rx="22" ry="22" width="260" height="90" fill="#c8ffe6" stroke="#00b894" stroke-width="4" filter="url(#soft)"/>
    <rect x="30" y="38" rx="18" ry="18" width="200" height="54" fill="#00c853"/>
    <text x="130" y="72" text-anchor="middle" class="pill">Safety</text>
  </g>

  <!-- Psychological -->
  <g transform="translate(420,430)">
    <text x="150" y="10" class="cap" fill="#ff9800" font-size="16">Psychological dimension</text>
    <rect x="0" y="20" rx="22" ry="22" width="300" height="90" fill="#ffe6c7" stroke="#ff9800" stroke-width="4" filter="url(#soft)"/>
    <rect x="30" y="38" rx="18" ry="18" width="240" height="54" fill="#ff8f2d"/>
    <text x="150" y="72" text-anchor="middle" class="pill">Downshift</text>
  </g>

  <!-- Right: Quality of Life -->
  <g transform="translate(770,170)">
    <text x="100" y="-20" class="cap" fill="#5f9ea0" font-size="18">QUALITY OF LIFE</text>
    <rect x="0" y="0" rx="26" ry="26" width="180" height="230" fill="#fff" stroke="#6fa28e" stroke-width="3" filter="url(#soft)"/>
    <g transform="translate(0,120)">
      <rect x="0" y="0" rx="26" ry="26" width="180" height="110" fill="#5f8f75"/>
      <text x="90" y="70" text-anchor="middle" class="score">+12</text>
    </g>
    <g transform="translate(14,24)">
      <text class="tiny" x="0" y="0">+12 from Social</text>
      <text class="tiny" x="0" y="18">+3 from Physical</text>
      <text class="tiny" x="0" y="36">-6 from Environmental</text>
      <text class="tiny" x="0" y="54">+3 from Psychological</text>
    </g>
  </g>

  <!-- Small grey badges on nodes -->
  <g>
    <g transform="translate(740,78)">
      <circle cx="0" cy="0" r="18" fill="#bdbdbd"/>
      <text x="0" y="5" text-anchor="middle" class="cap" font-size="14" fill="#fff">+6</text>
    </g>
    <g transform="translate(670,240)">
      <circle cx="0" cy="0" r="18" fill="#bdbdbd"/>
      <text x="0" y="5" text-anchor="middle" class="cap" font-size="14" fill="#fff">+3</text>
    </g>
    <g transform="translate(660,372)">
      <circle cx="0" cy="0" r="18" fill="#bdbdbd"/>
      <text x="0" y="5" text-anchor="middle" class="cap" font-size="14" fill="#fff">-3</text>
    </g>
    <g transform="translate(620,520)">
      <circle cx="0" cy="0" r="18" fill="#bdbdbd"/>
      <text x="0" y="5" text-anchor="middle" class="cap" font-size="14" fill="#fff">+3</text>
    </g>
  </g>

  <!-- ========== Arrows from Intervention to dimensions ========== -->
  <!-- to Social (x2, green curve) -->
  <path d="M240,245 C350,140 370,110 440,90" fill="none" stroke="#19a974" stroke-width="6" marker-end="url(#arrowGreen)"/>
  <text x="335" y="155" class="cap" font-size="18" fill="#19a974">x2</text>

  <!-- to Physical (x1, green curve) -->
  <path d="M240,245 C330,235 350,230 420,240" fill="none" stroke="#19a974" stroke-width="6" marker-end="url(#arrowGreen)"/>
  <text x="330" y="232" class="cap" font-size="18" fill="#19a974">x1</text>

  <!-- to Environmental (x-1, red curve) -->
  <path d="M240,245 C320,300 350,315 420,330" fill="none" stroke="#e85959" stroke-width="6" marker-end="url(#arrowRed)"/>
  <text x="320" y="300" class="cap" font-size="18" fill="#e85959">x-1</text>

  <!-- to Psychological (x1, green curve) -->
  <path d="M240,245 C320,360 360,400 420,460" fill="none" stroke="#19a974" stroke-width="6" marker-end="url(#arrowGreen)"/>
  <text x="320" y="380" class="cap" font-size="18" fill="#19a974">x1</text>

  <!-- ========== Arrows from dimensions to QoL ========== -->
  <!-- Social -> QoL (x2) -->
  <path d="M740,90 C800,140 820,220 860,280" fill="none" stroke="#19a974" stroke-width="8" marker-end="url(#arrowGreen)"/>
  <text x="790" y="130" class="cap" font-size="18" fill="#19a974">x2</text>

  <!-- Physical -> QoL (x1) -->
  <path d="M660,230 C740,230 760,250 860,280" fill="none" stroke="#19a974" stroke-width="6" marker-end="url(#arrowGreen)"/>
  <text x="745" y="225" class="cap" font-size="18" fill="#19a974">x1</text>

  <!-- Environmental -> QoL (x2) -->
  <path d="M680,360 C760,340 780,320 860,300" fill="none" stroke="#19a974" stroke-width="8" marker-end="url(#arrowGreen)"/>
  <text x="755" y="330" class="cap" font-size="18" fill="#19a974">x2</text>

  <!-- Psychological -> QoL (x1) -->
  <path d="M720,480 C780,440 800,420 860,360" fill="none" stroke="#19a974" stroke-width="6" marker-end="url(#arrowGreen)"/>
  <text x="780" y="430" class="cap" font-size="18" fill="#19a974">x1</text>

</svg>
'''

st.components.v1.html(svg, height=600, scrolling=False)
