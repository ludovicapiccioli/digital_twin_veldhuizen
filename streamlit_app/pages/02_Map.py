# pages/02_Map.py
from pathlib import Path
import json
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

GJ_NEIGH = DATA_DIR / "neighbourhoods_veld.geojson"
GJ_MUNI  = DATA_DIR / "municipality_ede.geojson"
GJ_WIJK  = DATA_DIR / "wijkenbuurtenwijken.geojson"     # optional
GJ_VELD  = DATA_DIR / "wijk_boundary_veld.geojson"      # optional
CATALOG  = DATA_DIR / "variables_catalog.csv"

MAP_HEIGHTS = {"Half-page": 460, "Normal": 700, "Full-page": 1000}

# --------------------------------------------------------------------------------------
# HELPERS
# --------------------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_catalog(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    need = {"dimension","label","column","unit"}
    miss = need - set(df.columns)
    if miss:
        raise ValueError(f"variables_catalog.csv missing columns: {miss}")
    return df

@st.cache_data(show_spinner=False)
def load_geojson(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def iter_coords(geom):
    """Yield (lon, lat) tuples from Polygon/MultiPolygon coordinate arrays."""
    t = geom.get("type")
    coords = geom.get("coordinates", [])
    if t == "Polygon":
        for ring in coords:
            for x, y in ring:
                yield (x, y)
    elif t == "MultiPolygon":
        for poly in coords:
            for ring in poly:
                for x, y in ring:
                    yield (x, y)

def bounds_of_geojson(geojson):
    """Return [[south, west], [north, east]] bounds for fit_bounds."""
    xs, ys = [], []
    for feat in geojson.get("features", []):
        for x, y in iter_coords(feat.get("geometry", {})):
            xs.append(x); ys.append(y)
    if not xs or not ys:
        # Fallback: center on Ede-ish
        return [[52.01, 5.56], [52.08, 5.72]]
    west, east = min(xs), max(xs)
    south, north = min(ys), max(ys)
    return [[south, west], [north, east]]

def fmt_num(x: float, hi: float) -> str:
    if x is None or not np.isfinite(x):
        return "n/a"
    decimals = 0 if hi >= 100 else 2
    return f"{x:,.{decimals}f}"

def add_outline(geojson, fmap, name, color="#111111", weight=1.2, dash=None, pane=None):
    """Draw outlines visible on top but NON-INTERACTIVE (no hover blocking)."""
    if not geojson or not geojson.get("features"):
        return
    kw = {}
    if pane:
        kw["pane"] = pane
    folium.GeoJson(
        data=geojson,
        name=name,
        style_function=lambda f: {
            "fillOpacity": 0,
            "color": color,
            "weight": weight,
            "className": "nohit-outline",
            **({"dashArray": dash} if dash else {}),
        },
        **kw,
    ).add_to(fmap)

def extract_series(geojson, prop):
    vals = []
    for f in geojson.get("features", []):
        v = pd.to_numeric(f.get("properties", {}).get(prop), errors="coerce")
        vals.append(v)
    return pd.Series(vals, dtype="float64")

# --------------------------------------------------------------------------------------
# UI
# --------------------------------------------------------------------------------------
st.set_page_config(page_title="Ede – Veldhuizen map", layout="wide")

# Existence checks
missing = [p for p in [GJ_NEIGH, GJ_MUNI, CATALOG] if not p.exists()]
if missing:
    st.error("Missing required files:\n" + "\n".join(f"- {m}" for m in missing))
    st.stop()

try:
    catalog = load_catalog(CATALOG)
    neigh_gj = load_geojson(GJ_NEIGH)
    muni_gj  = load_geojson(GJ_MUNI)
    wijk_gj  = load_geojson(GJ_WIJK) if GJ_WIJK.exists() else None
    veld_gj  = load_geojson(GJ_VELD) if GJ_VELD.exists() else None
except Exception as e:
    st.error(f"Failed to load data.\n\n{e}")
    st.stop()

# Sidebar
st.sidebar.header("Choose indicator")
dimensions = catalog["dimension"].dropna().unique().tolist()
dim = st.sidebar.selectbox("Dimension", dimensions, index=0)

sub = catalog[catalog["dimension"] == dim].copy()
sel_label = st.sidebar.selectbox("Variable", sub["label"].tolist(), index=0)
row = sub[sub["label"] == sel_label].iloc[0]
var_col = row["column"]
unit    = str(row.get("unit","")).strip()

color_mode = st.sidebar.radio("Color mode", ["Continuous gradient", "Discrete classes"], index=0)
if color_mode == "Discrete classes":
    classes = st.sidebar.selectbox("Classification", ["Equal interval","Quantile"], index=0)
    k = st.sidebar.slider("Number of classes", 5, 9, 7)
else:
    classes = "Equal interval"; k = 7

st.sidebar.markdown("---")
show_wijk = st.sidebar.checkbox("Show district (wijk) boundaries", True)
show_muni = st.sidebar.checkbox("Show municipality outline", True)
show_veld = st.sidebar.checkbox("Highlight Veldhuizen outline", True)

size = st.sidebar.radio("Map size", list(MAP_HEIGHTS.keys()), index=0, horizontal=True)
map_height = MAP_HEIGHTS[size]

# --------------------------------------------------------------------------------------
# DATA PREP
# --------------------------------------------------------------------------------------
# Ensure property exists in both layers
prop_missing = []
for layer_name, gj in [("neighbourhoods_veld", neigh_gj), ("municipality_ede", muni_gj)]:
    if not gj.get("features"):
        prop_missing.append(f"{layer_name} (no features)")
    else:
        if var_col not in gj["features"][0]["properties"]:
            prop_missing.append(f"{layer_name}.{var_col}")

if prop_missing:
    st.error("Selected column not found in layers:\n" + "\n".join(f"- {p}" for p in prop_missing))
    st.stop()

neigh_vals = extract_series(neigh_gj, var_col)
muni_val   = pd.to_numeric(muni_gj["features"][0]["properties"].get(var_col), errors="coerce")

# Shared range for both layers
combined = pd.concat([neigh_vals, pd.Series([muni_val])], ignore_index=True)
if combined.dropna().empty:
    vmin, vmax = 0.0, 1.0
else:
    vmin = float(np.nanmin(combined))
    vmax = float(np.nanmax(combined))
if vmin == vmax:
    vmin -= 0.5; vmax += 0.5

# Palettes
palette_cont = ["#f7fbff","#deebf7","#c6dbef","#9ecae1","#6baed6","#3182bd","#08519c"]
palette_disc = ["#fff5f0","#fcbba1","#fc9272","#fb6a4a","#ef3b2c","#cb181d","#99000d","#67000d","#3b0008"]

# Build color scale & color function
if color_mode == "Continuous gradient":
    cmap = LinearColormap(colors=palette_cont, vmin=vmin, vmax=vmax)

    def color_for_value(x):
        if x is None or pd.isna(x):
            return "#cccccc"
        return cmap(float(x))
else:
    # bins for discrete classes
    clean = combined.dropna().to_numpy()
    if clean.size == 0:
        bins = [vmin, vmax]
    else:
        if classes.lower().startswith("quantile"):
            qs = np.linspace(0, 1, k + 1)
            bins = list(np.quantile(clean, qs))
            if len(pd.unique(bins)) < 3:
                bins = list(np.linspace(vmin, vmax, k + 1))
        else:
            bins = list(np.linspace(vmin, vmax, k + 1))

    rng = abs(bins[-1] - bins[0])
    if rng >= 100:  bins = [round(b, 0) for b in bins]
    elif rng >= 10: bins = [round(b, 1) for b in bins]
    else:           bins = [round(b, 2) for b in bins]

    colors = palette_disc[:k]
    cmap = StepColormap(colors=colors, index=bins, vmin=bins[0], vmax=bins[-1])

    def color_for_value(x):
        if x is None or pd.isna(x):
            return "#cccccc"
        x = float(x)
        for i in range(len(bins) - 1):
            last = (i == len(bins) - 2)
            if (x >= bins[i]) and (x < bins[i+1] or (last and x <= bins[i+1])):
                return colors[i]
        return colors[-1]

# Format for tooltips
hi = float(np.nanmax(neigh_vals)) if np.isfinite(np.nanmax(neigh_vals)) else 0.0
def build_neigh_tt(props):
    name = props.get("buurtnaam", "Neighbourhood")
    val = pd.to_numeric(props.get(var_col), errors="coerce")
    return (
        "<div style='font-size:12px'>"
        f"<b>{name}</b><br>"
        "<span style='opacity:.8'>Neighbourhood in Veldhuizen (Ede)</span><br>"
        f"{sel_label}" + (f" [{unit}]" if unit else "") + f": {fmt_num(val, hi)}"
        "</div>"
    )

# Copy GeoJSON and inject formatted tooltip property
def with_tooltips(gj, tooltip_prop="_tt", label="neigh"):
    gj2 = {"type": "FeatureCollection", "features": []}
    for f in gj.get("features", []):
        pf = {
            "type": "Feature",
            "geometry": f.get("geometry"),
            "properties": dict(f.get("properties", {}))
        }
        if label == "neigh":
            pf["properties"][tooltip_prop] = build_neigh_tt(pf["properties"])
        else:
            # municipality
            mv = pd.to_numeric(pf["properties"].get(var_col), errors="coerce")
            pf["properties"][tooltip_prop] = (
                "<div style='font-size:12px'><b>Ede (municipality)</b><br>"
                f"{sel_label}" + (f" [{unit}]" if unit else "") + f": {fmt_num(mv, hi)}</div>"
            )
        gj2["features"].append(pf)
    return gj2

neigh_tt = with_tooltips(neigh_gj, "_tt", "neigh")
muni_tt  = with_tooltips(muni_gj, "_tt", "muni")

# --------------------------------------------------------------------------------------
# MAP (fit to municipality bounds) + PANES + NON-INTERACTIVE outlines + LABEL
# --------------------------------------------------------------------------------------
bounds = bounds_of_geojson(muni_gj)

m = folium.Map(
    location=[(bounds[0][0]+bounds[1][0])/2, (bounds[0][1]+bounds[1][1])/2],
    zoom_start=11,
    tiles="cartodbpositron",
    control_scale=False,
    scrollWheelZoom=True,
    doubleClickZoom=True,
    zoom_control=True,
)

# CSS / panes
m.get_root().header.add_child(Element("""
<style>
.nohit-outline { pointer-events: none !important; }
.leaflet-control-attribution { display:none !important; }
.leaflet-control-layers { display:none !important; }

/* Tooltips above labels */
.leaflet-tooltip-pane { z-index: 10050 !important; }
.leaflet-marker-pane  { z-index: 10040 !important; }  /* labels below tooltips */

/* Label style */
.map-perimeter-label {
  font-size: 14px; font-weight: 700; color: #111;
  text-shadow: 0 1px 2px rgba(255,255,255,0.85), 0 -1px 2px rgba(255,255,255,0.65);
  white-space: nowrap;
  pointer-events: none !important;
}

/* Remove focus ring */
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

folium.map.CustomPane("municipality-pane", z_index=300).add_to(m)   # below
folium.map.CustomPane("neighbourhoods-pane", z_index=400).add_to(m) # above
folium.map.CustomPane("outline-pane", z_index=500, pointer_events="none").add_to(m)
folium.map.CustomPane("label-pane", z_index=450, pointer_events="none").add_to(m)

# Municipality fill
m_muni_val = float(muni_val) if pd.notna(muni_val) else np.nan
folium.GeoJson(
    data=muni_tt,
    name=f"Ede (municipality) – {sel_label}",
    pane="municipality-pane",
    style_function=lambda feature: {
        "fillOpacity": 0.55,
        "fillColor": color_for_value(m_muni_val),
        "color": "#555555",
        "weight": 0.7,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["_tt"], aliases=[""], sticky=True, labels=False,
        parse_html=True, localize=False,
        style=("background-color:white; color:#111; padding:6px 8px; "
               "border-radius:4px; box-shadow:0 1px 2px rgba(0,0,0,0.25);")
    ),
).add_to(m)

# Neighbourhoods fill
folium.GeoJson(
    data=neigh_tt,
    name=f"Veldhuizen neighbourhoods – {sel_label}",
    pane="neighbourhoods-pane",
    style_function=lambda feature: {
        "fillOpacity": 0.85,
        "fillColor": color_for_value(pd.to_numeric(feature['properties'].get(var_col), errors='coerce')),
        "color": "#333333",
        "weight": 0.6,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["_tt"], aliases=[""], sticky=True, labels=False,
        parse_html=True, localize=False,
        style=("background-color:white; color:#111; padding:6px 8px; "
               "border-radius:4px; box-shadow:0 1px 2px rgba(0,0,0,0.25);")
    ),
).add_to(m)

# Optional outlines
if show_wijk and GJ_WIJK.exists():
    add_outline(wijk_gj, m, "Wijk boundaries", color="#222222", weight=1.0, pane="outline-pane")
if show_muni:
    add_outline(muni_gj, m, "Municipality outline", color="#000000", weight=1.6, pane="outline-pane")
if show_veld and GJ_VELD.exists():
    add_outline(veld_gj, m, "Veldhuizen outline", color="#1f77b4", weight=2.2, pane="outline-pane")

# Legend
cmap.caption = f"{sel_label}" + (f"  [{unit}]" if unit and unit != "-" else "")
cmap.add_to(m)

# Fit map to municipality
m.fit_bounds(bounds, padding=(12, 12))

# Info line above the map
mode_str = "gradient" if color_mode == "Continuous gradient" else f"{classes.lower()}, k={k}"
st.markdown(
    "**Variable:** " + f"{sel_label}"
    + (f"  •  **Unit:** {unit}" if unit else "")
    + f"  •  **Color mode:** {mode_str}"
)

# Render
st_folium(m, height=map_height, width=None, returned_objects=[], key="map_static")

# Attribution
st.caption("Basemap: CARTO Positron • © OpenStreetMap contributors")
