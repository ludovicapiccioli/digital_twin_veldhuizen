# pages/02_Map.py
from pathlib import Path
import json
import math
import numpy as np
import pandas as pd
import streamlit as st
import folium
from branca.colormap import LinearColormap, StepColormap
from branca.element import Element
from streamlit_folium import st_folium

# --------------------------------------------------------------------------------------
# PATHS
# --------------------------------------------------------------------------------------
APP_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = APP_ROOT / "data"

NEIGH_PATH = DATA_DIR / "neighbourhoods_veld.geojson"
MUNI_PATH  = DATA_DIR / "municipality_ede.geojson"
WIJK_PATH  = DATA_DIR / "wijkenbuurtenwijken.geojson"        # outlines (optional)
VELD_PATH  = DATA_DIR / "wijk_boundary_veld.geojson"         # outline (optional)
CATALOG_CSV = DATA_DIR / "variables_catalog.csv"

MAP_HEIGHTS = {"Half-page": 460, "Normal": 700, "Full-page": 1000}

# --------------------------------------------------------------------------------------
# GEOJSON HELPERS (no GeoPandas needed)
# --------------------------------------------------------------------------------------
def load_geojson(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def features(gj):
    return gj.get("features", []) if isinstance(gj, dict) else []

def get_bounds_of_feature(feat):
    """Compute [minx, miny, maxx, maxy] of a single GeoJSON feature (Polygon/MultiPolygon)."""
    geom = feat.get("geometry", {})
    gtype = geom.get("type", "")
    coords = geom.get("coordinates", [])
    xs, ys = [], []
    if gtype == "Polygon":
        rings = coords
    elif gtype == "MultiPolygon":
        rings = [ring for poly in coords for ring in poly]
    else:
        rings = []
    for ring in rings:
        for x, y in ring:
            xs.append(x); ys.append(y)
    if not xs:
        return None
    return [min(xs), min(ys), max(xs), max(ys)]

def bounds_union(gj):
    """Union bounds of a GeoJSON FeatureCollection."""
    b = None
    for f in features(gj):
        fb = get_bounds_of_feature(f)
        if fb is None:
            continue
        if b is None:
            b = fb
        else:
            b = [min(b[0], fb[0]), min(b[1], fb[1]), max(b[2], fb[2]), max(b[3], fb[3])]
    return b

def centroid_of_bounds(bounds):
    """Center of a bbox [minx,miny,maxx,maxy] -> (lat, lon)."""
    minx, miny, maxx, maxy = bounds
    return [(miny + maxy) / 2.0, (minx + maxx) / 2.0]

def largest_polygon_centroid(gj):
    """
    Approximate label point for Veldhuizen outline:
    pick largest polygon by area and return centroid of its outer ring (no shapely).
    """
    best_area = -1.0
    best_centroid = None

    for feat in features(gj):
        geom = feat.get("geometry", {})
        gtype = geom.get("type", "")
        if gtype not in ("Polygon", "MultiPolygon"):
            continue
        polys = []
        if gtype == "Polygon":
            polys = [geom.get("coordinates", [])]
        elif gtype == "MultiPolygon":
            polys = geom.get("coordinates", [])

        for poly in polys:
            if not poly:
                continue
            ring = poly[0]  # exterior
            if len(ring) < 3:
                continue
            # polygon signed area + centroid (shoelace formula)
            area = 0.0
            cx = 0.0
            cy = 0.0
            n = len(ring)
            for i in range(n):
                x1, y1 = ring[i]
                x2, y2 = ring[(i + 1) % n]
                cross = x1 * y2 - x2 * y1
                area += cross
                cx += (x1 + x2) * cross
                cy += (y1 + y2) * cross
            area *= 0.5
            if abs(area) < 1e-12:
                continue
            cx /= (6.0 * area)
            cy /= (6.0 * area)
            if abs(area) > best_area:
                best_area = abs(area)
                best_centroid = (cy, cx)  # (lat, lon)

    return best_centroid  # (lat, lon) or None

# --------------------------------------------------------------------------------------
# COLORING / BINS
# --------------------------------------------------------------------------------------
PALETTE_BASE = ["#fff5f0","#fcbba1","#fc9272","#fb6a4a","#ef3b2c","#cb181d","#99000d","#67000d","#3b0008"]

def collect_values_from_neigh_and_muni(neigh_gj, muni_gj, var):
    vals = []
    for f in features(neigh_gj):
        v = f.get("properties", {}).get(var)
        try:
            v = float(v)
            if math.isfinite(v):
                vals.append(v)
        except Exception:
            pass
    # municipal value is single feature
    if features(muni_gj):
        v = features(muni_gj)[0].get("properties", {}).get(var)
        try:
            v = float(v)
            if math.isfinite(v):
                vals.append(v)
        except Exception:
            pass
    return vals

def make_discrete_bins(vals, mode="Equal interval", k=7):
    if not vals:
        return [0.0, 1.0]
    v = np.array(vals, dtype=float)
    v = v[np.isfinite(v)]
    if v.size == 0:
        return [0.0, 1.0]

    if mode.lower().startswith("quantile"):
        qs = np.linspace(0, 1, k + 1)
        bins = list(np.quantile(v, qs))
        # if repeated quantiles (flat data), fallback to equal interval
        if len(pd.unique(bins)) < 3:
            bins = list(np.linspace(v.min(), v.max(), k + 1))
    else:
        bins = list(np.linspace(v.min(), v.max(), k + 1))

    rng = abs(bins[-1] - bins[0])
    if rng >= 100:  bins = [round(b, 0) for b in bins]
    elif rng >= 10: bins = [round(b, 1) for b in bins]
    else:           bins = [round(b, 2) for b in bins]
    return bins

def colormap_and_range(neigh_vals, discrete=False, mode="Equal interval", k=7):
    if not neigh_vals:
        vmin, vmax = 0.0, 1.0
    else:
        v = np.array(neigh_vals, dtype=float)
        v = v[np.isfinite(v)]
        if v.size == 0:
            vmin, vmax = 0.0, 1.0
        else:
            vmin, vmax = float(v.min()), float(v.max())
            if vmin == vmax:
                vmin -= 0.5
                vmax += 0.5

    if not discrete:
        cmap = LinearColormap(colors=PALETTE_BASE, vmin=vmin, vmax=vmax)
        return cmap, (vmin, vmax)

    # discrete
    bins = make_discrete_bins(neigh_vals, mode=mode, k=k)
    colors = PALETTE_BASE[:k]
    cmap = StepColormap(colors=colors, index=bins, vmin=bins[0], vmax=bins[-1])
    return cmap, (bins[0], bins[-1])

def color_for_value(x, cmap, vmin=None, vmax=None, discrete=False):
    if x is None:
        return "#cccccc"
    try:
        xx = float(x)
        if not math.isfinite(xx):
            return "#cccccc"
    except Exception:
        return "#cccccc"

    if not discrete:
        return cmap(xx)
    # StepColormap handles classing internally on call
    return cmap(xx)

def fmt_value(x, hi_guess=100.0):
    try:
        xx = float(x)
    except Exception:
        return "n/a"
    if not math.isfinite(xx):
        return "n/a"
    decimals = 0 if hi_guess >= 100 else 2
    return f"{xx:,.{decimals}f}"

# --------------------------------------------------------------------------------------
# UI
# --------------------------------------------------------------------------------------
st.set_page_config(page_title="Map • Ede–Veldhuizen", layout="wide")

# Existence checks
missing = [p.name for p in [NEIGH_PATH, MUNI_PATH, CATALOG_CSV] if not p.exists()]
if missing:
    st.error(f"Missing required files in /data: {', '.join(missing)}")
    st.stop()

# Load
neigh_gj = load_geojson(NEIGH_PATH)
muni_gj  = load_geojson(MUNI_PATH)
wijk_gj  = load_geojson(WIJK_PATH) if WIJK_PATH.exists() else None
veld_gj  = load_geojson(VELD_PATH) if VELD_PATH.exists() else None
catalog  = pd.read_csv(CATALOG_CSV)

# Sidebar
st.sidebar.header("Choose indicator")
dimensions = catalog["dimension"].dropna().unique().tolist()
dim = st.sidebar.selectbox("Dimension", dimensions, index=0)

sub = catalog[catalog["dimension"] == dim].copy()
label = st.sidebar.selectbox("Variable", sub["label"].tolist(), index=0)
row = sub[sub["label"] == label].iloc[0]
var_col = row["column"]
unit    = str(row.get("unit", "")).strip()

# Color mode
color_mode = st.sidebar.radio("Color mode", ["Continuous gradient", "Discrete classes"], index=0)
if color_mode == "Discrete classes":
    classes = st.sidebar.selectbox("Classification", ["Equal interval", "Quantile"], index=0)
    k = st.sidebar.slider("Number of classes", 5, 9, 7)
    discrete = True
else:
    classes = "Equal interval"
    k = 7
    discrete = False

st.sidebar.markdown("---")
show_wijk = st.sidebar.checkbox("Show district (wijk) boundaries", True)
show_muni = st.sidebar.checkbox("Show municipality outline", True)
show_veld = st.sidebar.checkbox("Highlight Veldhuizen outline", True)

size = st.sidebar.radio("Map size", list(MAP_HEIGHTS.keys()), index=0, horizontal=True)
map_height = MAP_HEIGHTS[size]

# --------------------------------------------------------------------------------------
# DATA PREP
# --------------------------------------------------------------------------------------
# Collect values (neighbourhoods + municipal single value) for common color scale
vals_all = []
# neigh values
for f in features(neigh_gj):
    v = f.get("properties", {}).get(var_col)
    try:
        v = float(v)
        if math.isfinite(v):
            vals_all.append(v)
    except Exception:
        pass
# municipal value
muni_val = None
if features(muni_gj):
    mv = features(muni_gj)[0].get("properties", {}).get(var_col)
    try:
        mv = float(mv)
        if math.isfinite(mv):
            muni_val = mv
            vals_all.append(mv)
    except Exception:
        pass

cmap, (vmin, vmax) = colormap_and_range(vals_all, discrete=discrete, mode=classes, k=k)

# Determine map center from municipality bbox
mb = bounds_union(muni_gj)
if mb:
    map_center = centroid_of_bounds(mb)  # (lat, lon)
else:
    nb = bounds_union(neigh_gj)
    map_center = centroid_of_bounds(nb) if nb else [52.05, 5.66]  # fallback roughly Ede

# --------------------------------------------------------------------------------------
# MAP + PANES + CSS
# --------------------------------------------------------------------------------------
m = folium.Map(
    location=map_center,
    zoom_start=12,
    tiles="cartodbpositron",
    control_scale=False,
    scrollWheelZoom=True,
    doubleClickZoom=True,
    zoom_control=True,
)

# CSS: keep outlines non-interactive; tidy UI; label styling
m.get_root().header.add_child(Element("""
<style>
.nohit-outline { pointer-events: none !important; }
.leaflet-control-attribution { display:none !important; }
.leaflet-control-layers { display:none !important; }

/* Tooltips above labels */
.leaflet-tooltip-pane { z-index: 10050 !important; }
.leaflet-marker-pane  { z-index: 10040 !important; }  /* labels below tooltips */

/* Outline label style */
.map-perimeter-label {
  font-size: 14px; font-weight: 700; color: #111;
  text-shadow: 0 1px 2px rgba(255,255,255,0.85), 0 -1px 2px rgba(255,255,255,0.65);
  white-space: nowrap;
  pointer-events: none !important;
}

/* Remove focus rectangle */
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

# Panes for draw order
folium.map.CustomPane("municipality-pane", z_index=300).add_to(m)    # BELOW
folium.map.CustomPane("neighbourhoods-pane", z_index=400).add_to(m)  # ABOVE
folium.map.CustomPane("label-pane", z_index=450, pointer_events="none").add_to(m)
folium.map.CustomPane("outline-pane", z_index=500, pointer_events="none").add_to(m)

# --------------------------------------------------------------------------------------
# ADD LAYERS
# --------------------------------------------------------------------------------------
# Helper to color a feature by property
def _fill_color(props):
    return color_for_value(props.get(var_col), cmap, vmin, vmax, discrete=discrete)

# Municipality polygon (single) with sticky tooltip & popup
if features(muni_gj):
    muni_props = features(muni_gj)[0].get("properties", {})
    muni_label = f"{label}" + (f" [{unit}]" if unit else "")
    muni_val_txt = fmt_value(muni_props.get(var_col), max(vals_all) if vals_all else 100)

    folium.GeoJson(
        muni_gj,
        name=f"Ede (municipality) – {label}",
        pane="municipality-pane",
        style_function=lambda feat: {
            "fillOpacity": 0.55,
            "fillColor": _fill_color(feat.get("properties", {})),
            "color": "#555555",
            "weight": 0.7,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=[],
            aliases=[],
            sticky=True, labels=False, parse_html=True,
            style=("background-color:white; color:#111; padding:6px 8px; "
                   "border-radius:4px; box-shadow:0 1px 2px rgba(0,0,0,0.25);"),
            localize=False,
            # custom HTML content via script - use folium popup below for robust
        ),
        popup=folium.GeoJsonPopup(
            fields=[],
            aliases=[],
            sticky=True, labels=False, parse_html=True,
            localize=False,
            # we inject a custom HTML in popup via lambda below
        ),
    ).add_to(m)
    # Set popup HTML explicitly (works reliably)
    folium.Popup(
        html=f"<div style='font-size:12px'><b>Ede (municipality)</b><br>{muni_label}: {muni_val_txt}</div>",
        max_width=280,
    ).add_to(m._children[list(m._children.keys())[-1]])  # attach to last added layer

# Veldhuizen neighbourhoods with hover + popup
# (Use tooltip fields for hover; popup repeats with nicer formatting)
neigh_label = f"{label}" + (f" [{unit}]" if unit else "")
folium.GeoJson(
    neigh_gj,
    name=f"Veldhuizen neighbourhoods – {label}",
    pane="neighbourhoods-pane",
    style_function=lambda feat: {
        "fillOpacity": 0.85,
        "fillColor": _fill_color(feat.get("properties", {})),
        "color": "#333333",
        "weight": 0.6,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["buurtnaam", var_col],
        aliases=["Neighbourhood", neigh_label],
        sticky=True, labels=False, parse_html=True, localize=False,
        style=("background-color:white; color:#111; padding:6px 8px; "
               "border-radius:4px; box-shadow:0 1px 2px rgba(0,0,0,0.25);")
    ),
    popup=folium.GeoJsonPopup(
        fields=["buurtnaam", var_col],
        aliases=["Neighbourhood", neigh_label],
        localize=False, labels=False, parse_html=True,
        style=("background-color:white; color:#111; padding:6px 8px; "
               "border-radius:4px; box-shadow:0 1px 2px rgba(0,0,0,0.25);")
    ),
).add_to(m)

# Optional outlines (non-interactive, on top)
def add_outline(gj, name, color="#111111", weight=1.2, dash=None, pane="outline-pane"):
    if not gj:
        return
    folium.GeoJson(
        gj,
        name=name,
        pane=pane,
        style_function=lambda f: {
            "fillOpacity": 0,
            "color": color,
            "weight": weight,
            **({"dashArray": dash} if dash else {}),
            "className": "nohit-outline",
        },
        highlight_function=None,
        tooltip=None,
    ).add_to(m)

if show_wijk and wijk_gj:
    add_outline(wijk_gj, "Wijk boundaries", color="#222222", weight=1.0)

if show_muni and muni_gj:
    add_outline(muni_gj, "Municipality outline", color="#000000", weight=1.6)

if show_veld and veld_gj:
    add_outline(veld_gj, "Veldhuizen outline", color="#E45756", weight=2.4)  # RED

# Perimeter label: "Ede–Veldhuizen"
if veld_gj:
    pt = largest_polygon_centroid(veld_gj)  # (lat, lon)
    if pt:
        lat, lon = pt
        # Use label pane if supported
        mk_kwargs = {}
        if "pane" in folium.Marker.__init__.__code__.co_varnames:
            mk_kwargs["pane"] = "label-pane"
        folium.Marker(
            location=[lat, lon],
            icon=folium.DivIcon(
                class_name="map-perimeter-label",
                html="Ede–Veldhuizen",
            ),
            **mk_kwargs,
        ).add_to(m)

# Legend
cmap.caption = f"{label}" + (f"  [{unit}]" if unit and unit != "-" else "")
cmap.add_to(m)

# Info line above the map
mode_str = "gradient" if not discrete else f"{classes.lower()}, k={k}"
st.markdown(
    "**Variable:** " + f"{label}"
    + (f"  •  **Unit:** {unit}" if unit else "")
    + f"  •  **Color mode:** {mode_str}"
)

# Render
st_folium(m, height=map_height, width=None, returned_objects=[], key="map_static")

st.caption("Basemap: CARTO Positron • © OpenStreetMap contributors")
