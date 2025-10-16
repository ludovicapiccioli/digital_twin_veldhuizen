# pages/02_Map.py
from __future__ import annotations
from pathlib import Path
import json
import numpy as np
import pandas as pd
import streamlit as st
import folium
from branca.colormap import LinearColormap, StepColormap
from branca.element import Element
from folium.features import DivIcon
import streamlit.components.v1 as components

# -------------------- Paths --------------------
APP_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = APP_ROOT / "data"
CATALOG_CSV = DATA_DIR / "variables_catalog.csv"

GJ_NEIGH = DATA_DIR / "neighbourhoods_veld.geojson"
GJ_MUNI  = DATA_DIR / "municipality_ede.geojson"
GJ_WIJK  = DATA_DIR / "wijkenbuurtenwijken.geojson"       # optional
GJ_VELD  = DATA_DIR / "wijk_boundary_veld.geojson"        # optional

MAP_HEIGHTS = {"Half-page": 460, "Normal": 700, "Full-page": 1000}
PALETTE_RED = [
    "#fff5f0","#fcbba1","#fc9272","#fb6a4a",
    "#ef3b2c","#cb181d","#99000d","#67000d","#3b0008"
]

# -------------------- Helpers --------------------
def load_geojson(p: Path) -> dict:
    with p.open("r", encoding="utf-8") as f:
        gj = json.load(f)
    if gj.get("type") != "FeatureCollection":
        raise ValueError(f"{p.name} must be a FeatureCollection")
    gj.setdefault("features", [])
    return gj

def feats(gj: dict):
    return gj.get("features", [])

def get_prop(f: dict, key: str, default=None):
    return f.get("properties", {}).get(key, default)

def extract_ring_points(geom: dict, out_list: list):
    if not geom: return
    t, c = geom.get("type"), geom.get("coordinates")
    if t == "Polygon" and c and c[0]:
        for pt in c[0]:
            if isinstance(pt, (list, tuple)) and len(pt) >= 2:
                out_list.append((float(pt[0]), float(pt[1])))  # (lon, lat)
    elif t == "MultiPolygon" and c and c[0] and c[0][0]:
        for pt in c[0][0]:
            if isinstance(pt, (list, tuple)) and len(pt) >= 2:
                out_list.append((float(pt[0]), float(pt[1])))

def bounds_of(gj: dict):
    pts = []
    for f in feats(gj):
        extract_ring_points(f.get("geometry"), pts)
    if not pts:
        # fallback box roughly around Ede
        return [[52.00, 5.58], [52.08, 5.74]]
    xs, ys = zip(*pts)  # lon, lat
    return [[float(min(ys)), float(min(xs))], [float(max(ys)), float(max(xs))]]

def top_label_point(gj: dict):
    pts = []
    for f in feats(gj):
        extract_ring_points(f.get("geometry"), pts)
    if not pts:
        return None
    lon, lat = max(pts, key=lambda xy: xy[1])
    return (lat, lon)

def combined_min_max(values):
    arr = np.array([v for v in values if v is not None and np.isfinite(v)], dtype=float)
    if arr.size == 0:
        return 0.0, 1.0
    vmin, vmax = float(arr.min()), float(arr.max())
    if vmin == vmax:
        vmin -= 0.5; vmax += 0.5
    return vmin, vmax

def color_for_value(x, cmap):
    try:
        xx = float(x)
        if not np.isfinite(xx):
            return "#cccccc"
    except Exception:
        return "#cccccc"
    return str(cmap(xx))

def add_outline(gj: dict, fmap, name, color="#111", weight=1.2, pane=None):
    if not gj or not feats(gj):
        return
    style = {
        "fillOpacity": 0,
        "color": color,
        "weight": weight,
        "className": "nohit-outline",
        "interactive": False
    }
    folium.GeoJson(
        data=gj, name=name, pane=pane,
        style_function=lambda f: style
    ).add_to(fmap)

# -------------------- UI --------------------
st.set_page_config(page_title="Map • Veldhuizen vs Ede", layout="wide")

# Kill any iframe border/focus ring Streamlit might add
st.markdown(
    "<style>iframe[title='streamlit-iframe']{border:0!important;outline:none!important;box-shadow:none!important;}</style>",
    unsafe_allow_html=True,
)

missing = [p for p in [CATALOG_CSV, GJ_NEIGH, GJ_MUNI] if not p.exists()]
if missing:
    st.error("Missing required files: " + ", ".join(p.name for p in missing))
    st.stop()

catalog = pd.read_csv(CATALOG_CSV)
need = {"dimension","label","column","unit"}
miss = need - set(catalog.columns)
if miss:
    st.error(f"variables_catalog.csv missing columns: {miss}")
    st.stop()

neigh_gj = load_geojson(GJ_NEIGH)
muni_gj  = load_geojson(GJ_MUNI)
wijk_gj  = load_geojson(GJ_WIJK) if GJ_WIJK.exists() else {"type":"FeatureCollection","features":[]}
veld_gj  = load_geojson(GJ_VELD) if GJ_VELD.exists() else {"type":"FeatureCollection","features":[]}

st.sidebar.header("Choose indicator")
dimensions = sorted(pd.Series(catalog["dimension"]).dropna().unique().tolist())
sel_dim = st.sidebar.selectbox("Dimension", dimensions, index=0)

subset = catalog[catalog["dimension"] == sel_dim].copy()
labels = subset["label"].tolist()
sel_label = st.sidebar.selectbox("Variable", labels, index=0)

row = subset[subset["label"] == sel_label].iloc[0]
var_col = str(row["column"])
unit    = str(row.get("unit","")).strip()

color_mode = st.sidebar.radio("Color mode", ["Continuous gradient", "Discrete classes"], index=0)
if color_mode == "Discrete classes":
    classes = st.sidebar.selectbox("Classification", ["Equal interval","Quantile"], index=0)
    k = st.sidebar.slider("Number of classes", 5, 9, 7)
else:
    classes, k = "Equal interval", 7

st.sidebar.markdown("---")
show_wijk = st.sidebar.checkbox("Show district (wijk) boundaries", True)
show_muni_outline = st.sidebar.checkbox("Show municipality outline", True)
show_veld_outline = st.sidebar.checkbox("Highlight Veldhuizen outline", True)
size = st.sidebar.radio("Map size", list(MAP_HEIGHTS.keys()), index=0, horizontal=True)
map_height = MAP_HEIGHTS[size]

# -------------------- Values & colormap --------------------
neigh_vals = []
for f in feats(neigh_gj):
    v = get_prop(f, var_col, None)
    try:
        neigh_vals.append(float(v))
    except Exception:
        neigh_vals.append(None)

muni_vals = []
for f in feats(muni_gj):
    v = get_prop(f, var_col, None)
    try:
        muni_vals.append(float(v))
    except Exception:
        muni_vals.append(None)

# Use a single municipality value if any; combine for vmin/vmax
muni_val = next((v for v in muni_vals if v is not None and np.isfinite(v)), None)
combined = neigh_vals + ([muni_val] if muni_val is not None else [])
vmin, vmax = combined_min_max(combined)

if color_mode == "Continuous gradient":
    cmap = LinearColormap(colors=PALETTE_RED, vmin=vmin, vmax=vmax)
else:
    finite_vals = [x for x in combined if x is not None and np.isfinite(x)]
    if classes.lower().startswith("quantile") and len(finite_vals) >= k:
        qs = np.linspace(0, 1, k + 1)
        bins = list(np.quantile(finite_vals, qs))
        for i in range(1, len(bins)):
            if bins[i] <= bins[i-1]:
                bins[i] = bins[i-1] + 1e-9
    else:
        bins = list(np.linspace(vmin, vmax, k + 1))
    rng = abs(bins[-1]-bins[0])
    if rng >= 100:  bins = [round(b,0) for b in bins]
    elif rng >= 10: bins = [round(b,1) for b in bins]
    else:           bins = [round(b,2) for b in bins]
    cmap = StepColormap(colors=PALETTE_RED[:k], index=bins, vmin=bins[0], vmax=bins[-1])

# -------------------- Tooltip fields --------------------
# Normalise name field
for f in feats(neigh_gj):
    p = f.setdefault("properties", {})
    p["buurtnaam"] = (
        p.get("buurtnaam") or p.get("Buurtnaam") or p.get("name") or p.get("NAAM") or "Unknown"
    )

vals_clean = [v for v in neigh_vals if v is not None and np.isfinite(v)]
maxv = max(vals_clean) if vals_clean else None
decimals = 0 if (maxv is not None and maxv >= 100) else 2

def fmt_unit_label(label: str, unit: str) -> str:
    u = (f" ({unit})" if unit and unit != "-" else "")
    return f"{label}{u}"

# Per-neighbourhood: format values + extra lines
for f in feats(neigh_gj):
    p = f.setdefault("properties", {})
    try:
        val = float(p.get(var_col, None))
        if not np.isfinite(val):
            raise ValueError
        p["_valtxt"] = f"{val:,.{decimals}f}"
    except Exception:
        p["_valtxt"] = "n/a"
    p["_subtitle"] = "Neighbourhood in Ede-Veldhuizen"
    p["_valpair"]  = f"{fmt_unit_label(sel_label, unit)}: {p['_valtxt']}"

# Per-municipality feature: ensure ALL features get the tooltip fields
for f in feats(muni_gj):
    p = f.setdefault("properties", {})
    try:
        mval = float(p.get(var_col, None))
        if not np.isfinite(mval):
            raise ValueError
        p["_valtxt"] = f"{mval:,.{decimals}f}"
    except Exception:
        p["_valtxt"] = "n/a"
    p["_muniname"] = p.get("gemeentenaam", "Ede (municipality)")
    p["_title"]    = "Ede (municipality)"
    p["_valpair"]  = f"{fmt_unit_label(sel_label, unit)}: {p['_valtxt']}"

# -------------------- Map --------------------
m = folium.Map(
    location=[52.04, 5.66],  # fallback; we’ll fit to Ede next
    zoom_start=11,
    tiles="cartodbpositron",
    control_scale=False,
    scrollWheelZoom=True,
    doubleClickZoom=True,
    zoom_control=True,
)

# CSS: keep tooltips above; remove attribution & layers; remove focus rings
m.get_root().header.add_child(Element("""
<style>
.nohit-outline { pointer-events: none !important; }
.leaflet-control-attribution { display:none !important; }
.leaflet-control-layers { display:none !important; }
.leaflet-tooltip-pane { z-index: 10050 !important; }
.leaflet-marker-pane  { z-index: 10040 !important; }

.map-perimeter-label {
  font-size: 14px; font-weight: 700; color: #111;
  text-shadow: 0 1px 2px rgba(255,255,255,0.85), 0 -1px 2px rgba(255,255,255,0.65);
  white-space: nowrap;
  pointer-events: none !important;
}

.leaflet-container:focus, .leaflet-overlay-pane svg:focus, .leaflet-interactive:focus, .leaflet-marker-icon:focus, .leaflet-control a:focus {
  outline: none !important;
  box-shadow: none !important;
}
</style>
"""))

# Layer panes
folium.map.CustomPane("municipality-pane", z_index=300).add_to(m)
folium.map.CustomPane("neighbourhoods-pane", z_index=400).add_to(m)
folium.map.CustomPane("outline-pane", z_index=500).add_to(m)
folium.map.CustomPane("label-pane", z_index=550).add_to(m)

# Municipality
folium.GeoJson(
    data=muni_gj,
    name=f"Ede (municipality) – {sel_label}",
    pane="municipality-pane",
    style_function=lambda feat: {
        "fillOpacity": 0.55,
        "fillColor": color_for_value(get_prop(feat, var_col, None), cmap),
        "color": "#555555",
        "weight": 0.7,
        "interactive": True,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["_title", "_valpair"],
        aliases=["", ""],
        sticky=True, labels=False, localize=False
    ),
).add_to(m)

# Neighbourhoods
folium.GeoJson(
    data=neigh_gj,
    name=f"Veldhuizen neighbourhoods – {sel_label}",
    pane="neighbourhoods-pane",
    style_function=lambda feat: {
        "fillOpacity": 0.85,
        "fillColor": color_for_value(get_prop(feat, var_col, None), cmap),
        "color": "#333333",
        "weight": 0.6,
    },
    highlight_function=lambda feat: {"fillOpacity": 0.92, "weight": 2.0, "color": "#222222"},
    tooltip=folium.GeoJsonTooltip(
        fields=["buurtnaam", "_subtitle", "_valpair"],
        aliases=["", "", ""],
        sticky=True, labels=False, localize=False
    ),
).add_to(m)

# Optional outlines
if show_wijk and feats(wijk_gj):
    add_outline(wijk_gj, m, "Wijk boundaries", color="#222", weight=1.0, pane="outline-pane")
if show_muni_outline:
    add_outline(muni_gj, m, "Municipality outline", color="#000", weight=1.6, pane="outline-pane")
if show_veld_outline and feats(veld_gj):
    add_outline(veld_gj, m, "Veldhuizen outline", color="#1f77b4", weight=2.2, pane="outline-pane")

# Perimeter label
tp = top_label_point(veld_gj) if feats(veld_gj) else None
if tp:
    lat, lon = tp
    folium.Marker(
        location=[lat, lon],
        icon=DivIcon(class_name="map-perimeter-label", html="Ede–Veldhuizen"),
        pane="label-pane",
    ).add_to(m)

# Legend (shared scale)
cmap.caption = f"{sel_label}" + (f"  [{unit}]" if unit and unit != "-" else "")
cmap.add_to(m)

# Fit to municipality bounds
m.fit_bounds(bounds_of(muni_gj))

# Info line in Streamlit
mode_str = "gradient" if color_mode == "Continuous gradient" else f"{classes.lower()}, k={k}"
st.markdown(
    "**Variable:** " + f"{sel_label}"
    + (f"  •  **Unit:** {unit}" if unit else "")
    + f"  •  **Color mode:** {mode_str}"
)

# -------------------- Render (map lowered) --------------------
TOP_SPACER_PX = 26  # adjust to taste (e.g., 18–32)

html = m.get_root().render()
html_wrapped = f"<div style='height:{TOP_SPACER_PX}px'></div>{html}"

components.html(html_wrapped, height=map_height + TOP_SPACER_PX, scrolling=False)
st.caption("Basemap: CARTO Positron • © OpenStreetMap contributors")
