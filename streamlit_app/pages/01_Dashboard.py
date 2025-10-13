# pages/01_Dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path

# ---------- Paths ----------
APP_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = APP_ROOT / "data"
CATALOG = DATA_DIR / "variables_catalog.csv"

# Use the GeoJSON files you’ll ship to Streamlit Cloud
NEIGH_JSON = DATA_DIR / "neighbourhoods_veld.geojson"
MUNI_JSON  = DATA_DIR / "municipality_ede.geojson"

st.set_page_config(page_title="Dashboard • Veldhuizen vs Ede", layout="wide")

# ---------- Load data ----------
@st.cache_data(show_spinner=False)
def load_catalog(path: Path) -> pd.DataFrame:
    cat = pd.read_csv(path)
    need = {"dimension", "label", "column", "unit"}
    miss = need - set(cat.columns)
    if miss:
        raise ValueError(f"variables_catalog.csv missing columns: {miss}")
    return cat

def _drop_geometry(df: gpd.GeoDataFrame) -> pd.DataFrame:
    cols = [c for c in df.columns if c != "geometry" and "geometry" not in str(df[c].dtype).lower()]
    return pd.DataFrame(df[cols])

@st.cache_data(show_spinner=False)
def load_layers(neigh_path: Path, muni_path: Path):
    neigh = gpd.read_file(neigh_path)
    muni  = gpd.read_file(muni_path)
    return _drop_geometry(neigh), _drop_geometry(muni)

# Existence checks
for pth, lbl in [(CATALOG, "Catalog CSV"),
                 (NEIGH_JSON, "Neighbourhoods GeoJSON"),
                 (MUNI_JSON, "Municipality GeoJSON")]:
    if not pth.exists():
        st.error(f"{lbl} not found at: {pth}")
        st.stop()

try:
    cat = load_catalog(CATALOG)
    neigh_df, muni_df = load_layers(NEIGH_JSON, MUNI_JSON)
except Exception as e:
    st.error(f"Failed to load data.\n\n{e}")
    st.stop()

# ---------- Basics ----------
name_col = "buurtnaam" if "buurtnaam" in neigh_df.columns else neigh_df.columns[0]
if name_col not in neigh_df.columns:
    st.error("Expected a neighbourhood name column (e.g., 'buurtnaam') not found.")
    st.stop()

# ---------- Sidebar ----------
st.sidebar.header("Choose indicators")
dims = sorted(cat["dimension"].unique().tolist())
sel_dim = st.sidebar.selectbox("Dimension", dims)

subset = cat[cat["dimension"] == sel_dim].copy()
labels = subset["label"].tolist()

sel_label = st.sidebar.selectbox("Variable", labels)
sel_row = subset[subset["label"] == sel_label].iloc[0]
var_col = sel_row["column"]
unit    = str(sel_row["unit"]).strip()

st.sidebar.markdown("---")
sort_order = st.sidebar.radio("Sort by", ["Descending", "Ascending", "Alphabetical"], horizontal=True)
show_labels = st.sidebar.checkbox("Show value labels on bars", value=True)

interactive = st.sidebar.checkbox(
    "Interactive hover (tooltips)", value=True,
    help="Shows neighbourhood and value on hover (uses Plotly if available)."
)

# Compact info line
bits = [f"**Variable:** {sel_label}"]
if unit:
    bits.append(f"**Unit:** {unit}")
bits.append(f"**Dimension:** {sel_dim}")
st.markdown("  •  ".join(bits))

# ---------- Data prep ----------
if var_col not in neigh_df.columns:
    st.error(f"Column `{var_col}` not found in neighbourhoods layer.")
    st.stop()

df = neigh_df[[name_col, var_col]].copy()
df[name_col] = df[name_col].astype(str)
df[var_col] = pd.to_numeric(df[var_col], errors="coerce")
df = df.dropna(subset=[var_col])

if df.empty:
    st.warning("All values for this variable are missing for the neighbourhoods.")
    st.stop()

# Municipal average
muni_value = np.nan
if var_col in muni_df.columns and len(muni_df) > 0:
    muni_value = pd.to_numeric(muni_df.iloc[0][var_col], errors="coerce")

# Sorting
if sort_order == "Alphabetical":
    df = df.sort_values(name_col, ascending=True, kind="mergesort")
else:
    df = df.sort_values(var_col, ascending=(sort_order == "Ascending"), kind="mergesort")

# ---------- Formatting helpers ----------
vals = df[var_col].to_numpy()
names = df[name_col].to_list()
n = len(names)
max_val = np.nanmax(vals)
min_val = np.nanmin(vals)

decimals = 0 if max_val >= 100 else 2
fmt = f"{{:,.{decimals}f}}"
title_var = f"{sel_label}" + (f" [{unit}]" if unit else "")

# x-limits (consider municipal average too)
candidates = [max_val]
if np.isfinite(muni_value):
    candidates.append(float(muni_value))
x_max = max(candidates) if candidates else max_val
x_pad = 0.08 * x_max if x_max > 0 else 1.0
x_upper = x_max + x_pad
x_lower = min(0.0, min_val, float(muni_value) if np.isfinite(muni_value) else 0.0)

# Dynamic sizing & left margin
row_height_in = 0.48
fig_height = max(3.6, row_height_in * n + 1.2)
max_label_len = max(len(s) for s in names) if names else 10
left_margin = min(0.35, 0.08 + 0.012 * max_label_len)

# Tidy frame for plotting
plot_df = df[[name_col, var_col]].rename(columns={name_col: "Neighbourhood", var_col: "Value"})
category_order = plot_df["Neighbourhood"].tolist()

# ---------- Interactive Plotly branch ----------
if interactive:
    try:
        import plotly.express as px
    except Exception:
        st.info("Interactive chart needs Plotly. Install with `pip install plotly`. Showing static chart instead…")
    else:
        try:
            height_px = int(fig_height * 140)

            fig = px.bar(
                plot_df.astype({"Value": float}),
                x="Value",
                y="Neighbourhood",
                orientation="h",
                category_orders={"Neighbourhood": category_order},
                template="plotly_white",
            )

            hovertemplate = (
                "<b>%{y}</b><br>"
                f"{sel_label}: "
                f"%{{x:,.{decimals}f}}"
                "<extra></extra>"
            )
            fig.update_traces(hovertemplate=hovertemplate)

            if show_labels:
                fig.update_traces(
                    text=[f"{v:,.{decimals}f}" for v in plot_df["Value"].values],
                    textposition="outside",
                    cliponaxis=False,
                )

            fig.update_xaxes(title_text=title_var, zeroline=False, fixedrange=True)
            fig.update_yaxes(automargin=True, title_text="", fixedrange=True)

            fig.update_layout(
                height=height_px,
                margin=dict(l=160, r=40, t=30, b=50),
                showlegend=False,
                bargap=0.15,
                uniformtext_minsize=8,
                uniformtext_mode="hide",
            )

            if np.isfinite(muni_value):
                xavg = float(muni_value)
                fig.add_vline(x=xavg, line_width=2, line_color="#D62728")
                fig.add_annotation(
                    x=xavg, y=1, xref="x", yref="paper",
                    text=f"Ede average: {xavg:,.{decimals}f}",
                    showarrow=False, xanchor="left", yanchor="bottom", xshift=6,
                    font=dict(color="#D62728"),
                )

            st.plotly_chart(
                fig, use_container_width=True,
                config=dict(displayModeBar=False, displaylogo=False, scrollZoom=False, doubleClick=False)
            )

            if np.isfinite(muni_value):
                st.caption(f"Tip: the red line marks the Ede municipal average for the selected indicator (≈ {fmt.format(float(muni_value))}).")
            else:
                st.caption("Tip: the red line marks the Ede municipal average for the selected indicator.")
            st.stop()

        except Exception as e:
            st.warning("Tried interactive Plotly chart but hit an error. Falling back to static chart below.")
            st.exception(e)

# ---------- Matplotlib chart (fallback / default) ----------
plt.style.use("default")
fig, ax = plt.subplots(figsize=(11.5, fig_height), dpi=140)

ypos = np.arange(n)
bar_height = 0.62
bar_color = "#2E6FF2"

ax.barh(ypos, vals, height=bar_height, color=bar_color)

ax.set_yticks(ypos)
ax.set_yticklabels(names)
ax.invert_yaxis()
ax.set_xlabel(title_var)
ax.set_ylabel("")
ax.set_xlim(x_lower, x_upper)

ax.grid(axis="x", linestyle=":", linewidth=0.8, alpha=0.6)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

if show_labels:
    span = (x_upper - x_lower)
    threshold = 0.15 * span
    for y, v in zip(ypos, vals):
        text = fmt.format(v)
        if v - x_lower > threshold:
            ax.text(v - 0.01*span, y, text, va="center", ha="right",
                    color="white", fontsize=9, fontweight="semibold")
        else:
            ax.text(v + 0.01*span, y, text, va="center", ha="left",
                    color="#222", fontsize=9)

if np.isfinite(muni_value):
    xavg = float(muni_value)
    ax.axvline(x=xavg, color="red", linewidth=2)
    ax.text(xavg, -0.7, f"Ede average: {fmt.format(xavg)}",
            color="red", ha="left", va="bottom", fontsize=10,
            bbox=dict(facecolor="white", alpha=0.85, edgecolor="none", pad=1.5))

fig.subplots_adjust(left=left_margin, right=0.97, top=0.92, bottom=0.12)
st.pyplot(fig)

if np.isfinite(muni_value):
    st.caption(f"Tip: the red line marks the Ede municipal average for the selected indicator (≈ {fmt.format(float(muni_value))}).")
else:
    st.caption("Tip: the red line marks the Ede municipal average for the selected indicator.")
