# pages/02_Map.py

from __future__ import annotations
from pathlib import Path
import json
import numpy as np
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from branca.colormap import LinearColormap, StepColormap
from branca.element import Element

# -------------------- Paths --------------------
APP_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = APP_ROOT / "data"
CATALOG_CSV = DATA_DIR / "variables_catalog.csv"

GJ_NEIGH = DATA_DIR / "neighbourhoods_veld.geojson"
GJ_MUNI  = DATA_DIR / "municipality_ede.geojson"
GJ_WIJK  = DATA_DIR / "wijkenbuurtenwijken.geojson"       # optional
GJ_VELD  = DATA_DIR / "wijk_boundary_veld.geojson"        # optional

MAP_HEIGHTS = {"Half-page": 460, "Normal": 700, "Full-page": 1000}
PALETTE_RED = ["#fff5f0","#fcbba1","#fc9272","#fb6a4a","#ef3b2c","#cb181d","#99000d","#67000d","#3b0008"]

# -------------------- Helpers --------------------
def load_geojson(p: Path) -> dict:
    with p.open("r", encoding="utf-8") as f:
        gj = json.load(f)
    if gj.get("type") != "FeatureCollection":
        raise ValueError(f"{p.name} must be a FeatureCollection")
    gj.setdefault("features", [])
    return gj

def feats(gj: dict): return gj.get("features", [])

def get_prop(f: dict, key: str, default=None):
    return f.get("properties", {}).get(key, default)

def extract_ring_points(geom: dict, out_list: list):
    if not geom: return
    t, c = geom.get("type"), geom.get("coordinates")
    if t == "Polygon" and c and c[0]:
        for pt in c[0]:
            if isinstance(pt, (list, tuple)) and len(pt) >= 2:
                out_list.append((float(pt[0]), float(pt[1])))
    elif t == "MultiPolygon" and c and c[0] and c[0][0]:
        for pt in c[0][0]:
            if isinstance(pt, (list, tuple)) and len(pt) >= 2:
                out_list.append((float(pt[0]), float(pt[1])))

def center_of(gj: dict):
    pts = []
    for f in feats(gj):
        extract_ring_points(f.get("geometry"), pts)
    if not pts: return [52.04, 5.66]  # fallback
    xs, ys = zip(*pts)
    return [float(np.mean(ys)), float(np.mean(xs))]

def top_label_point(gj: dict):
    pts = []
    for f in feats(gj):
        extract_ring_points(f.get("geometry"), pts)
    if not pts: return None
    lon, lat = max(pts, key=lambda xy: xy[1])
    return (lat, lon)

def combined_min_max(values):
    arr = np.array([v for v in values if v is not None and np.isfinite(v)], dtype=float)
    if arr.size == 0: return 0.0, 1.0
    vmin, vmax = float(arr.min()), float(arr.max())
    if vmin == vmax: vmin -= 0.5; vmax += 0.5
    return vmin, vmax

def color_for_value(x, cmap):
    try:
        xx = float(x)
        if not np.isfinite(xx): return "#cccccc"
    except Exception:
        return "#cccccc"
    return str(cmap(xx))

def add_outline(gj: dict, fmap, name, color="#111", weight=1.2, dash=None, pane=None):
    if not gj or not feats(gj): return
    style = {"fillOpacity": 0, "color": color, "weight": weight, "className": "nohit-outline"}
    if dash: style["dashArray"] = dash
    kw = {"pane": pane} if pane else {}
    folium.GeoJson(data=gj, name=name, style_function=lambda f: style, **kw).add_to(fmap)

# -------------------- UI --------------------
st.set_page_config(page_title="Map • Veldhuizen vs Ede", layout="wide")

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
    try: neigh_vals.append(float(v))
    except Exception: neigh_vals.append(None)

muni_val = None
if feats(muni_gj):
    mv = get_prop(feats(muni_gj)[0], var_col, None)
    try: muni_val = float(mv)
    except Exception: muni_val = None

combined = neigh_vals + ([muni_val] if muni_val is not None else [])
vmin, vmax = combined_min_max(combined)

if color_mode == "Continuous gradient":
    cmap = LinearColormap(colors=PALETTE_RED, vmin=vmin, vmax=vmax)
else:
    finite_vals = [x for x in combined if x is not None and np.isfinite(x)]
    if classes.lower().startswith("quantile") and len(finite_vals) >= k:
        qs = np.linspace(0, 1, k + 1)
        bins = list(np.quantile(finite_vals, qs))
        # Avoid duplicate edges from tied quantiles
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

# -------------------- Robust tooltip fields --------------------
# Guarantee 'buurtnaam' exists for every feature and build _valtxt safely
for f in feats(neigh_gj):
    props = f.setdefault("properties", {})
    props["buurtnaam"] = (
        props.get("buurtnaam")
        or props.get("Buurtnaam")
        or props.get("name")
        or props.get("NAAM")
        or "Unknown"
    )

# Precompute a plain-text value column for robust tooltips
vals_clean = [v for v in neigh_vals if v is not None and np.isfinite(v)]
maxv = max(vals_clean) if vals_clean else None
decimals = 0 if (maxv is not None and maxv >= 100) else 2

for f in feats(neigh_gj):
    props = f.setdefault("properties", {})
    try:
        val = float(props.get(var_col, None))
        if not np.isfinite(val):
            raise ValueError
        props["_valtxt"] = f"{val:,.{decimals}f}"
    except Exception:
        props["_valtxt"] = "n/a"

if feats(muni_gj):
    props = feats(muni_gj)[0].setdefault("properties", {})
    try:
        mval = float(props.get(var_col, None))
        if not np.isfinite(mval):
            raise ValueError
        props["_valtxt"] = f"{mval:,.{decimals}f}"
    except Exception:
        props["_valtxt"] = "n/a"

# -------------------- Map --------------------
m = folium.Map(
    location=center_of(muni_gj),
    zoom_start=11,
    tiles="cartodbpositron",
    control_scale=False,
    scrollWheelZoom=True,
    doubleClickZoom=True,
    zoom_control=True,
)

# CSS: keep outlines non-hit, label above fill, tooltips topmost
m.get_root().header.add_child(Element("""
<style>
.nohit-outline { pointer-events: none !important; }
.leaflet-control-attribution { display:none !important; }
.leaflet-control-layers { display:none !important; }
/* Tooltips above everything */
.leaflet-tooltip-pane { z-index: 10050 !important; }
/* Custom label pane (via class) above polygons but below tooltips */
.custom-label-pane { z-index: 1000 !important; pointer-events: none !important; }
</style>
"""))

# Panes: backdrop (non-interactive fill), neighbourhoods, outlines
folium.map.CustomPane("backdrop-pane", z_index=300, pointer_events="none").add_to(m)   # municipality fill (no hit)
folium.map.CustomPane("neighbourhoods-pane", z_index=410).add_to(m)                   # interactive hover
folium.map.CustomPane("outline-pane", z_index=500, pointer_events="none").add_to(m)   # outlines

# Municipality (non-interactive fill so it never blocks hover)
folium.GeoJson(
    data=muni_gj,
    name=f"Ede (municipality) – {sel_label}",
    pane="backdrop-pane",
    style_function=lambda feat: {
        "fillOpacity": 0.55,
        "fillColor": color_for_value(get_prop(feat, var_col, None), cmap),
        "color": "#555555",
        "weight": 0.7,
    },
).add_to(m)

# Neighbourhoods (hover tooltip + popup)
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
        fields=["buurtnaam", "_valtxt"],
        aliases=[
            "Neighbourhood",
            f"{sel_label}" + (f" ({unit})" if unit and unit != "-" else "")
        ],
        sticky=True, labels=False, localize=False
    ),
    popup=folium.GeoJsonPopup(
        fields=["buurtnaam", "_valtxt"],
        aliases=[
            "Neighbourhood",
            f"{sel_label}" + (f" ({unit})" if unit and unit != "-" else "")
        ],
        labels=False, localize=False
    ),
).add_to(m)

# Outlines (never intercept mouse)
if show_wijk and feats(wijk_gj):
    add_outline(wijk_gj, m, "Wijk boundaries", color="#222", weight=1.0, pane="outline-pane")
if show_muni_outline:
    add_outline(muni_gj, m, "Municipality outline", color="#000", weight=1.6, pane="outline-pane")
if show_veld_outline and feats(veld_gj):
    add_outline(veld_gj, m, "Veldhuizen outline", color="#1f77b4", weight=2.2, pane="outline-pane")

# Perimeter label (Ede–Veldhuizen) ABOVE polygons (use DivIcon with higher z via CSS class)
tp = top_label_point(veld_gj) if feats(veld_gj) else None
if tp:
    lat, lon = tp
    folium.Marker(
        location=[lat, lon],
        icon=folium.DivIcon(
            class_name="custom-label-pane",
            html=(
                "<div style=\"font-size:14px;font-weight:700;color:#111;"
                "text-shadow:0 1px 2px rgba(255,255,255,0.85),0 -1px 2px rgba(255,255,255,0.65);"
                "white-space:nowrap;\">Ede–Veldhuizen</div>"
            ),
        ),
    ).add_to(m)

# Legend
cmap.caption = f"{sel_label}" + (f"  [{unit}]" if unit and unit != "-" else "")
cmap.add_to(m)

# Info line
mode_str = "gradient" if color_mode == "Continuous gradient" else f"{classes.lower()}, k={k}"
st.markdown(
    "**Variable:** " + f"{sel_label}"
    + (f"  •  **Unit:** {unit}" if unit else "")
    + f"  •  **Color mode:** {mode_str}"
)

# Render
st_folium(m, height=map_height, width=None, returned_objects=[], key="map_static")
st.caption("Basemap: CARTO Positron • © OpenStreetMap contributors")
