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

# --------------------------------------------------------------------------------------
# PATHS
# --------------------------------------------------------------------------------------
APP_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = APP_ROOT / "data"
CATALOG_CSV = DATA_DIR / "variables_catalog.csv"

GJ_NEIGH = DATA_DIR / "neighbourhoods_veld.geojson"
GJ_MUNI  = DATA_DIR / "municipality_ede.geojson"
GJ_WIJK  = DATA_DIR / "wijkenbuurtenwijken.geojson"       # optional
GJ_VELD  = DATA_DIR / "wijk_boundary_veld.geojson"        # optional

MAP_HEIGHTS = {"Half-page": 460, "Normal": 700, "Full-page": 1000}

# Same red palette you used before (light -> dark)
PALETTE_RED = ["#fff5f0","#fcbba1","#fc9272","#fb6a4a","#ef3b2c","#cb181d","#99000d","#67000d","#3b0008"]

# --------------------------------------------------------------------------------------
# HELPERS (pure-GeoJSON, no GeoPandas)
# --------------------------------------------------------------------------------------
def load_geojson(p: Path) -> dict:
    with p.open("r", encoding="utf-8") as f:
        gj = json.load(f)
    if gj.get("type") != "FeatureCollection":
        raise ValueError(f"{p.name} must be a FeatureCollection")
    # Ensure 'features' exists
    gj.setdefault("features", [])
    return gj

def features(gj: dict):
    return gj.get("features", [])

def get_prop(f: dict, key: str, default=None):
    return f.get("properties", {}).get(key, default)

def fmt_num(x, hi_hint=100.0) -> str:
    try:
        xx = float(x)
    except Exception:
        return "n/a"
    if not np.isfinite(xx):
        return "n/a"
    return f"{xx:,.0f}" if hi_hint >= 100 else f"{xx:,.2f}"

def extract_all_coords(geom: dict, out_list: list):
    """Collect all [lon,lat] pairs from (Multi)Polygon/LineString shells (no shapely)."""
    if geom is None:
        return
    gtype = geom.get("type")
    coords = geom.get("coordinates")
    if gtype in ("Point", "MultiPoint", "LineString"):
        for pt in (coords if gtype != "Point" else [coords]):
            if isinstance(pt, (list, tuple)) and len(pt) >= 2:
                out_list.append((float(pt[0]), float(pt[1])))
    elif gtype == "MultiLineString":
        for line in coords or []:
            for pt in line or []:
                if isinstance(pt, (list, tuple)) and len(pt) >= 2:
                    out_list.append((float(pt[0]), float(pt[1])))
    elif gtype == "Polygon":
        # take exterior ring (coords[0]) for label/centroid heuristics
        if coords and isinstance(coords[0], list):
            for pt in coords[0]:
                if isinstance(pt, (list, tuple)) and len(pt) >= 2:
                    out_list.append((float(pt[0]), float(pt[1])))
    elif gtype == "MultiPolygon":
        # take first polygon's exterior ring for heuristics
        if coords and isinstance(coords[0], list) and coords[0] and isinstance(coords[0][0], list):
            for pt in coords[0][0]:
                if isinstance(pt, (list, tuple)) and len(pt) >= 2:
                    out_list.append((float(pt[0]), float(pt[1])))
    # (Other geometry types ignored here for simplicity)

def rough_center(gj: dict) -> list[float]:
    """Heuristic center: average of exterior coordinates from all features."""
    pts = []
    for f in features(gj):
        extract_all_coords(f.get("geometry"), pts)
    if not pts:
        # fallback to Ede-ish center if empty
        return [52.04, 5.66]
    xs, ys = zip(*pts)
    return [float(np.mean(ys)), float(np.mean(xs))]  # [lat, lon]

def top_label_point(gj: dict) -> tuple[float,float] | None:
    """Find the 'highest' (max lat) point from the Veldhuizen outline for the label."""
    pts = []
    for f in features(gj):
        extract_all_coords(f.get("geometry"), pts)
    if not pts:
        return None
    # pts are (lon, lat); pick max lat
    lon, lat = max(pts, key=lambda xy: xy[1])
    return (lat, lon)

def build_catalog(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    need = {"dimension","label","column","unit"}
    miss = need - set(df.columns)
    if miss:
        raise ValueError(f"variables_catalog.csv missing columns: {miss}")
    return df

def combined_min_max(values: list[float]) -> tuple[float,float]:
    arr = np.array([v for v in values if v is not None and np.isfinite(v)], dtype=float)
    if arr.size == 0:
        return 0.0, 1.0
    vmin, vmax = float(arr.min()), float(arr.max())
    if vmin == vmax:
        vmin -= 0.5
        vmax += 0.5
    return vmin, vmax

def color_for_value(x, cmap, discrete=False):
    if x is None:
        return "#cccccc"
    try:
        xx = float(x)
        if not np.isfinite(xx):
            return "#cccccc"
    except Exception:
        return "#cccccc"
    # both LinearColormap and StepColormap are callable
    return str(cmap(xx))

def add_outline_geojson(gj: dict, fmap, name, color="#111111", weight=1.2, dash=None, pane=None):
    if not gj or not features(gj):
        return
    style = {
        "fillOpacity": 0,
        "color": color,
        "weight": weight,
        "className": "nohit-outline",
    }
    if dash:
        style["dashArray"] = dash
    kw = {}
    if pane:
        kw["pane"] = pane
    folium.GeoJson(
        data=gj,
        name=name,
        style_function=lambda f: style,
        **kw,
    ).add_to(fmap)

# --------------------------------------------------------------------------------------
# PAGE
# --------------------------------------------------------------------------------------
st.set_page_config(page_title="Map • Veldhuizen vs Ede", layout="wide")

# Inputs existence
missing = [p for p in [CATALOG_CSV, GJ_NEIGH, GJ_MUNI] if not p.exists()]
if missing:
    st.error("Missing required files: " + ", ".join(p.name for p in missing))
    st.stop()

# Load catalog & GeoJSONs
try:
    catalog = build_catalog(CATALOG_CSV)
    neigh_gj = load_geojson(GJ_NEIGH)
    muni_gj  = load_geojson(GJ_MUNI)
    wijk_gj  = load_geojson(GJ_WIJK) if GJ_WIJK.exists() else {"type":"FeatureCollection","features":[]}
    veld_gj  = load_geojson(GJ_VELD) if GJ_VELD.exists() else {"type":"FeatureCollection","features":[]}
except Exception as e:
    st.error(f"Failed to load data.\n\n{e}")
    st.stop()

# Sidebar controls
st.sidebar.header("Choose indicator")
dimensions = sorted(pd.Series(catalog["dimension"]).dropna().unique().tolist())
sel_dim = st.sidebar.selectbox("Dimension", dimensions, index=0)

subset = catalog[catalog["dimension"] == sel_dim].copy()
labels = subset["label"].tolist()
sel_label = st.sidebar.selectbox("Variable", labels, index=0)

sel_row = subset[subset["label"] == sel_label].iloc[0]
var_col = str(sel_row["column"])
unit    = str(sel_row.get("unit","")).strip()

color_mode = st.sidebar.radio("Color mode", ["Continuous gradient", "Discrete classes"], index=0)
if color_mode == "Discrete classes":
    classes = st.sidebar.selectbox("Classification", ["Equal interval","Quantile"], index=0)
    k = st.sidebar.slider("Number of classes", 5, 9, 7)
else:
    classes, k = "Equal interval", 7  # placeholders

st.sidebar.markdown("---")
show_wijk = st.sidebar.checkbox("Show district (wijk) boundaries", True)
show_muni_outline = st.sidebar.checkbox("Show municipality outline", True)
show_veld_outline = st.sidebar.checkbox("Highlight Veldhuizen outline", True)

size = st.sidebar.radio("Map size", list(MAP_HEIGHTS.keys()), index=0, horizontal=True)
map_height = MAP_HEIGHTS[size]

# --------------------------------------------------------------------------------------
# Build values list for common scale (neigh + muni)
# --------------------------------------------------------------------------------------
neigh_vals = []
for f in features(neigh_gj):
    v = get_prop(f, var_col, None)
    try:
        v = float(v)
    except Exception:
        v = None
    neigh_vals.append(v)

muni_val = None
if features(muni_gj):
    mv = get_prop(features(muni_gj)[0], var_col, None)
    try:
        muni_val = float(mv)
    except Exception:
        muni_val = None

combined_vals = neigh_vals + ([muni_val] if muni_val is not None else [])
vmin, vmax = combined_min_max(combined_vals)

# Colormap
if color_mode == "Continuous gradient":
    cmap = LinearColormap(colors=PALETTE_RED, vmin=vmin, vmax=vmax)
    discrete = False
else:
    # Bins
    finite_vals = [x for x in combined_vals if x is not None and np.isfinite(x)]
    if classes.lower().startswith("quantile") and len(finite_vals) >= k:
        qs = np.linspace(0, 1, k + 1)
        bins = list(np.quantile(finite_vals, qs))
    else:
        bins = list(np.linspace(vmin, vmax, k + 1))

    # Round edges nicely
    rng = abs(bins[-1] - bins[0])
    if rng >= 100:  bins = [round(b, 0) for b in bins]
    elif rng >= 10: bins = [round(b, 1) for b in bins]
    else:           bins = [round(b, 2) for b in bins]

    cmap = StepColormap(colors=PALETTE_RED[:k], index=bins, vmin=bins[0], vmax=bins[-1])
    discrete = True

# --------------------------------------------------------------------------------------
# Prebuild _tt HTML tooltips to match your old style
# --------------------------------------------------------------------------------------
# “hi” to pick decimals
hi_hint = max([x for x in neigh_vals if x is not None and np.isfinite(x)], default=0.0)

# Neighbourhood features
for f in features(neigh_gj):
    props = f.setdefault("properties", {})
    name = str(props.get("buurtnaam", ""))
    val  = props.get(var_col, None)
    val_txt = fmt_num(val, hi_hint)
    unit_txt = f" [{unit}]" if unit else ""
    props["_tt"] = (
        "<div style='font-size:12px'>"
        f"<b>{name}</b><br>"
        "<span style='opacity:.8'>Neighbourhood in Veldhuizen (Ede)</span><br>"
        f"{sel_label}{unit_txt}: {val_txt}"
        "</div>"
    )

# Municipality feature
if features(muni_gj):
    props = features(muni_gj)[0].setdefault("properties", {})
    mtxt = fmt_num(props.get(var_col, None), hi_hint)
    unit_txt = f" [{unit}]" if unit else ""
    props["_tt"] = (
        "<div style='font-size:12px'><b>Ede (municipality)</b><br>"
        f"{sel_label}{unit_txt}: {mtxt}</div>"
    )

# --------------------------------------------------------------------------------------
# MAP
# --------------------------------------------------------------------------------------
center = rough_center(muni_gj)  # [lat, lon]
m = folium.Map(
    location=center,
    zoom_start=11,
    tiles="cartodbpositron",
    control_scale=False,
    scrollWheelZoom=True,
    doubleClickZoom=True,
    zoom_control=True,
)

# CSS panes & styles (nohit outlines, tooltip/readability, red legend stays)
m.get_root().header.add_child(Element("""
<style>
.nohit-outline { pointer-events: none !important; }
.leaflet-control-attribution { display:none !important; }
.leaflet-control-layers { display:none !important; }

/* Put tooltips over labels */
.leaflet-tooltip-pane { z-index: 10050 !important; }
.leaflet-marker-pane  { z-index: 10040 !important; }

/* Perimeter label style */
.map-perimeter-label {
  font-size: 14px; font-weight: 700; color: #111;
  text-shadow: 0 1px 2px rgba(255,255,255,0.85), 0 -1px 2px rgba(255,255,255,0.65);
  white-space: nowrap;
  pointer-events: none !important;
}

/* Remove black focus rectangle */
.leaflet-container:focus,
.leaflet-overlay-pane svg:focus,
.leaflet-interactive:focus,
.leaflet-marker-icon:focus,
.leaflet-control a:focus {
  outline: none !important;
  box-shadow: none !important;
}
</style>
"""))

# Draw order panes
folium.map.CustomPane("municipality-pane", z_index=300).add_to(m)   # BACK
folium.map.CustomPane("neighbourhoods-pane", z_index=400).add_to(m) # FRONT
folium.map.CustomPane("outline-pane", z_index=500, pointer_events="none").add_to(m)
folium.map.CustomPane("label-pane", z_index=450, pointer_events="none").add_to(m)

# Municipality (filled, popup only so it doesn't fight with neigh tooltip)
folium.GeoJson(
    data=muni_gj,
    name=f"Ede (municipality) – {sel_label}",
    pane="municipality-pane",
    style_function=lambda feat: {
        "fillOpacity": 0.55,
        "fillColor": color_for_value(get_prop(feat, var_col, None), cmap, discrete),
        "color": "#555555",
        "weight": 0.7,
    },
    highlight_function=lambda feat: {"fillOpacity": 0.65, "weight": 1.2, "color": "#444444"},
    popup=folium.GeoJsonPopup(
        fields=["_tt"], aliases=[""], labels=False, parse_html=True,
        style=("background-color:white; color:#111; padding:6px 8px; "
               "border-radius:4px; box-shadow:0 1px 2px rgba(0,0,0,0.25);")
    ),
).add_to(m)

# Veldhuizen neighbourhoods (tooltip + popup + thicker on hover)
folium.GeoJson(
    data=neigh_gj,
    name=f"Veldhuizen neighbourhoods – {sel_label}",
    pane="neighbourhoods-pane",
    style_function=lambda feat: {
        "fillOpacity": 0.85,
        "fillColor": color_for_value(get_prop(feat, var_col, None), cmap, discrete),
        "color": "#333333",
        "weight": 0.6,
    },
    highlight_function=lambda feat: {"fillOpacity": 0.92, "weight": 2.0, "color": "#222222"},
    tooltip=folium.GeoJsonTooltip(
        fields=["_tt"], aliases=[""], sticky=True, labels=False, parse_html=True,
        style=("background-color:white; color:#111; padding:6px 8px; "
               "border-radius:4px; box-shadow:0 1px 2px rgba(0,0,0,0.25);")
    ),
    popup=folium.GeoJsonPopup(
        fields=["_tt"], aliases=[""], labels=False, parse_html=True,
        style=("background-color:white; color:#111; padding:6px 8px; "
               "border-radius:4px; box-shadow:0 1px 2px rgba(0,0,0,0.25);")
    ),
).add_to(m)

# Optional non-interactive outlines (TOP)
if show_wijk and features(GJ_WIJK.exists() and wijk_gj or {"features": []}):
    add_outline_geojson(wijk_gj, m, "Wijk boundaries", color="#222222", weight=1.0, pane="outline-pane")
if show_muni_outline:
    add_outline_geojson(muni_gj, m, "Municipality outline", color="#000000", weight=1.6, pane="outline-pane")
if show_veld_outline and features(GJ_VELD.exists() and veld_gj or {"features": []}):
    add_outline_geojson(veld_gj, m, "Veldhuizen outline", color="#1f77b4", weight=2.2, pane="outline-pane")

# Perimeter label: "Ede–Veldhuizen"
tp = top_label_point(veld_gj) if features(veld_gj) else None
if tp:
    lat, lon = tp
    # pane is supported by newer Folium; ignore if not
    try:
        folium.Marker(
            location=[lat, lon],
            icon=folium.DivIcon(class_name="map-perimeter-label", html='Ede–Veldhuizen'),
            pane="label-pane",
        ).add_to(m)
    except TypeError:
        folium.Marker(
            location=[lat, lon],
            icon=folium.DivIcon(class_name="map-perimeter-label", html='Ede–Veldhuizen'),
        ).add_to(m)

# Legend (red scale)
unit_txt = f"  [{unit}]" if unit and unit != "-" else ""
cmap.caption = f"{sel_label}{unit_txt}"
cmap.add_to(m)

# Info line above map
mode_str = "gradient" if color_mode == "Continuous gradient" else f"{classes.lower()}, k={k}"
st.markdown(
    "**Variable:** " + f"{sel_label}"
    + (f"  •  **Unit:** {unit}" if unit else "")
    + f"  •  **Color mode:** {mode_str}"
)

# Render map
st_folium(m, height=map_height, width=None, returned_objects=[], key="map_static")

# Attribution
st.caption("Basemap: CARTO Positron • © OpenStreetMap contributors")
