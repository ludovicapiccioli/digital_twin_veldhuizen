import streamlit as st
import pandas as pd
import numpy as np
import json
from pathlib import Path

import folium
from folium.features import GeoJson, GeoJsonTooltip
from streamlit_folium import st_folium
import branca.colormap as cm

# ---------------- Paths & files ----------------
APP_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = APP_ROOT / "data"

GJ_NEIGH = DATA_DIR / "neighbourhoods_veld.geojson"     # polygons + vars (per buurt)
GJ_MUNI  = DATA_DIR / "municipality_ede.geojson"        # single polygon + same vars (Ede avg)
GJ_WIJK  = DATA_DIR / "wijkenbuurtenwijken.geojson"     # district (wijk) boundaries (lines or polys)
GJ_VELD  = DATA_DIR / "wijk_boundary_veld.geojson"      # Veldhuizen outline (line or poly)
CATALOG  = DATA_DIR / "variables_catalog.csv"           # dimension,label,column,unit

st.set_page_config(page_title="Map • Veldhuizen vs Ede", layout="wide")
st.title("Map — Veldhuizen neighbourhoods vs. Ede (municipal average)")

# ---------------- Helpers ----------------
@st.cache_data(show_spinner=False)
def load_geojson(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data(show_spinner=False)
def load_catalog(path: Path) -> pd.DataFrame:
    cat = pd.read_csv(path)
    need = {"dimension","label","column","unit"}
    miss = need - set(cat.columns)
    if miss:
        raise ValueError(f"variables_catalog.csv missing columns: {miss}")
    return cat

def features_to_df(gj: dict) -> pd.DataFrame:
    rows = []
    for feat in gj["features"]:
        props = feat.get("properties", {})
        rows.append(props)
    return pd.DataFrame(rows)

def gj_bounds(gj: dict):
    # Compute [south, west, north, east] across Polygon/MultiPolygon
    import math
    south, west =  math.inf,  math.inf
    north, east = -math.inf, -math.inf

    def consume_coords(coords):
        nonlocal south, west, north, east
        for x, y in coords:
            west  = min(west,  x)
            east  = max(east,  x)
            south = min(south, y)
            north = max(north, y)

    for feat in gj["features"]:
        geom = feat.get("geometry", {})
        gtype = geom.get("type")
        coords = geom.get("coordinates", [])
        if gtype == "Polygon":
            for ring in coords:
                consume_coords(ring)
        elif gtype == "MultiPolygon":
            for poly in coords:
                for ring in poly:
                    consume_coords(ring)
    return [[south, west], [north, east]]

def colormap_and_range(values: pd.Series, n=6):
    vals = pd.to_numeric(values, errors="coerce").dropna()
    if vals.empty:
        return None, (0, 1)
    vmin, vmax = float(vals.min()), float(vals.max())
    if vmin == vmax:
        vmax = vmin + 1e-9
    cmap = cm.linear.Viridis_06.scale(vmin, vmax)  # 6-class viridis
    return cmap, (vmin, vmax)

# ---------------- Load data ----------------
try:
    cat  = load_catalog(CATALOG)
    gj_neigh = load_geojson(GJ_NEIGH)
    gj_muni  = load_geojson(GJ_MUNI)
    # outlines are optional; handle missing gracefully
    gj_wijk  = load_geojson(GJ_WIJK) if GJ_WIJK.exists() else None
    gj_veld  = load_geojson(GJ_VELD) if GJ_VELD.exists() else None
except Exception as e:
    st.error(f"Failed to load data.\n\n{e}")
    st.stop()

df_neigh = features_to_df(gj_neigh)
df_muni  = features_to_df(gj_muni)

# Pick a name field to show in tooltips/labels
name_field_candidates = ["buurtnaam", "name", "naam"]
name_field = next((c for c in name_field_candidates if c in df_neigh.columns), None)
if name_field is None:
    st.error("Could not find a neighbourhood name field (e.g. 'buurtnaam') in neighbourhoods GeoJSON.")
    st.stop()

# ---------------- Sidebar controls ----------------
st.sidebar.header("Choose indicator")

dims = sorted(cat["dimension"].unique().tolist())
sel_dim = st.sidebar.selectbox("Dimension", dims)

subset = cat[cat["dimension"] == sel_dim].copy()
labels = subset["label"].tolist()

sel_label = st.sidebar.selectbox("Variable", labels)
sel_row   = subset[subset["label"] == sel_label].iloc[0]
var_col   = sel_row["column"]
unit      = str(sel_row["unit"]).strip()

# ---------------- Prepare values & color scale ----------------
if var_col not in df_neigh.columns:
    st.error(f"Selected column `{var_col}` not found in neighbourhoods data.")
    st.stop()

neigh_vals = pd.to_numeric(df_neigh[var_col], errors="coerce")
cmap, (vmin, vmax) = colormap_and_range(neigh_vals)
if cmap is None:
    st.warning("All values are missing for the selected variable.")
    st.stop()

# municipal average (single feature expected)
muni_val = np.nan
if var_col in df_muni.columns:
    try:
        muni_val = float(pd.to_numeric(df_muni.iloc[0][var_col], errors="coerce"))
    except Exception:
        muni_val = np.nan

# ---------------- Build map ----------------
bounds = gj_bounds(gj_neigh)
m = folium.Map(location=[(bounds[0][0]+bounds[1][0])/2, (bounds[0][1]+bounds[1][1])/2],
               zoom_start=13, tiles="cartodbpositron")

# Neighbourhood choropleth (styled via style_function to guarantee same scale)
def style_neigh(feature):
    val = feature.get("properties", {}).get(var_col, None)
    try:
        val = float(val)
    except Exception:
        val = None
    color = "#cccccc" if val is None or np.isnan(val) else cmap(val)
    return {
        "fillColor": color,
        "color": "#666666",
        "weight": 0.7,
        "fillOpacity": 0.8,
    }

tooltip_fields = [name_field, var_col]
tooltip_alias  = ["Neighbourhood", f"{sel_label} ({unit})" if unit else sel_label]

neigh_layer = GeoJson(
    gj_neigh,
    name=f"Neighbourhoods — {sel_label}",
    style_function=style_neigh,
    highlight_function=lambda f: {"weight": 2, "color": "#000000"},
    tooltip=GeoJsonTooltip(fields=tooltip_fields, aliases=tooltip_alias, localize=True)
)
neigh_layer.add_to(m)

# Municipality (single polygon) colored with SAME colormap
def style_muni(feature):
    val = muni_val
    color = "#cccccc" if val is None or np.isnan(val) else cmap(val)
    return {
        "fillColor": color,
        "color": "#444444",
        "weight": 1.2,
        "fillOpacity": 0.25,   # lighter so neighbourhoods stay visible on top
    }

muni_tip = GeoJsonTooltip(
    fields=["gemeentenaam"]+[var_col] if "gemeentenaam" in df_muni.columns else [var_col],
    aliases=["Municipality", f"Ede average — {sel_label} ({unit})" if unit else f"Ede average — {sel_label}"],
    localize=True
)
muni_layer = GeoJson(gj_muni, name="Municipality average (background)",
                     style_function=style_muni, tooltip=muni_tip)
muni_layer.add_to(m)

# Outlines (optional)
if gj_wijk is not None:
    GeoJson(
        gj_wijk,
        name="District boundaries (wijk)",
        style_function=lambda f: {"fillOpacity": 0, "color": "#000000", "weight": 1.2, "dashArray": "4,4"},
    ).add_to(m)

if gj_veld is not None:
    GeoJson(
        gj_veld,
        name="Veldhuizen outline",
        style_function=lambda f: {"fillOpacity": 0, "color": "#ff6f00", "weight": 2.5},
    ).add_to(m)

# Add consistent legend
cmap.caption = f"{sel_label}" + (f" [{unit}]" if unit else "")
cmap.add_to(m)

folium.LayerControl(collapsed=False).add_to(m)

# Fit bounds to neighbourhoods
m.fit_bounds(bounds, padding=(10, 10))

# ---------------- UI ----------------
st.subheader("Selected indicator")
st.markdown(
    f"**{sel_label}**" + (f" &nbsp;·&nbsp; _{unit}_ " if unit else "") +
    " — neighbourhoods are colored by value; the municipality is shown in the background with the **same** color scale."
)

st_folium(m, height=700, width=None)
