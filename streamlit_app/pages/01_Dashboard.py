# pages/01_Dashboard.py
import json
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# ---------- Paths ----------
APP_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = APP_ROOT / "data"

CATALOG = DATA_DIR / "variables_catalog.csv"
NEIGH_GJSON = DATA_DIR / "neighbourhoods_veld.geojson"
MUNI_GJSON  = DATA_DIR / "municipality_ede.geojson"

st.set_page_config(page_title="Dashboard • Veldhuizen vs Ede", layout="wide")

# ---------- Color constants ----------
COL_A   = "#E24B35"   # Veldhuizen A
COL_B   = "#F6A18A"   # Veldhuizen B 
COL_AVG = "#006400"   # Ede average 

# ---------- Helpers ----------
def geojson_to_table(path: Path) -> pd.DataFrame:
    """Read a GeoJSON and return a pandas DataFrame of feature properties."""
    with open(path, "r", encoding="utf-8") as f:
        gj = json.load(f)
    props = [feat.get("properties", {}) for feat in gj.get("features", [])]
    return pd.DataFrame(props)

@st.cache_data(show_spinner=False)
def load_catalog(path: Path) -> pd.DataFrame:
    cat = pd.read_csv(path)
    required = {"dimension", "label", "column", "unit"}
    missing = required - set(cat.columns)
    if missing:
        raise ValueError(f"variables_catalog.csv missing columns: {missing}")
    return cat

@st.cache_data(show_spinner=False)
def load_tables() -> tuple[pd.DataFrame, pd.DataFrame]:
    neigh_df = geojson_to_table(NEIGH_GJSON)
    muni_df  = geojson_to_table(MUNI_GJSON)
    return neigh_df, muni_df

# ---------- Load ----------
try:
    cat = load_catalog(CATALOG)
    neigh_df, muni_df = load_tables()
except Exception as e:
    st.error(f"Failed to load data.\n\n{e}")
    st.stop()

# Identify neighbourhood name column
name_col = "buurtnaam" if "buurtnaam" in neigh_df.columns else neigh_df.columns[0]
if name_col not in neigh_df.columns:
    st.error("Expected a neighbourhood name column (e.g., 'buurtnaam').")
    st.stop()

# ---------- Sidebar ----------
st.sidebar.header("Choose indicators")
dims = sorted(cat["dimension"].dropna().unique().tolist())
sel_dim = st.sidebar.selectbox("Dimension", dims)

subset = cat[cat["dimension"] == sel_dim].copy()
labels = subset["label"].tolist()

sel_label = st.sidebar.selectbox("Variable", labels)
sel_row = subset.loc[subset["label"] == sel_label].iloc[0]
var_col = sel_row["column"]
unit    = str(sel_row["unit"]).strip()

st.sidebar.markdown("---")
sort_order  = st.sidebar.radio("Sort by", ["Descending", "Ascending", "Alphabetical"], horizontal=True)
show_labels = st.sidebar.checkbox("Show value labels on bars", value=True)

# Small info line
bits = [f"**Variable:** {sel_label}"]
if unit:
    bits.append(f"**Unit:** {unit}")
bits.append(f"**Dimension:** {sel_dim}")
st.markdown("  •  ".join(bits))

# ---------- Data prep ----------
if var_col not in neigh_df.columns:
    st.error(f"Column `{var_col}` not found in neighbourhoods table.")
    st.stop()

df = neigh_df[[name_col, var_col]].copy()
df[name_col] = df[name_col].astype(str)
df[var_col]  = pd.to_numeric(df[var_col], errors="coerce")
df = df.dropna(subset=[var_col])
if df.empty:
    st.warning("All values are missing for this indicator.")
    st.stop()

# --- Tag Veldhuizen A/B ---
_a_names = {"de horsten", "de burgen"}
name_norm = df[name_col].str.strip().str.casefold()
df["is_A"] = name_norm.isin(_a_names)
df["Group"] = np.where(df["is_A"], "Veldhuizen A", "Veldhuizen B")
df["LabelName"] = df[name_col] + np.where(df["is_A"], " (A)", " (B)")

# Municipal average 
muni_value = np.nan
if var_col in muni_df.columns and len(muni_df) > 0:
    muni_value = pd.to_numeric(muni_df.iloc[0][var_col], errors="coerce")

# Sorting
if sort_order == "Alphabetical":
    df = df.sort_values("LabelName", ascending=True, kind="mergesort")
else:
    df = df.sort_values(var_col, ascending=(sort_order == "Ascending"), kind="mergesort")

# ---------- Formatting ----------
vals   = df[var_col].to_numpy()
names  = df["LabelName"].tolist()
n      = len(names)
vmax   = np.nanmax(vals)
vmin   = np.nanmin(vals)
dec    = 0 if vmax >= 100 else 2
fmt    = f"{{:,.{dec}f}}"
xlabel = f"{sel_label}" + (f" [{unit}]" if unit else "")

HEIGHT_SCALE = 0.90  

# Axis bounds with headroom 
cands  = [vmax]
if np.isfinite(muni_value):
    cands.append(float(muni_value))
xmax    = max(cands)
pad     = 0.08 * xmax if xmax > 0 else 1.0
x_upper = xmax + pad
x_lower = min(0.0, vmin, float(muni_value) if np.isfinite(muni_value) else 0.0)

# ---------- Try interactive Plotly, else Matplotlib ----------
rendered_interactive = False
try:
    import plotly.express as px

    height_px = int(max(3.6, 0.48 * n + 1.2) * 140 * HEIGHT_SCALE)

    pldf = df.rename(columns={"LabelName": "Neighbourhood", var_col: "Value"})[
        ["Neighbourhood", "Value", "Group"]
    ].astype({"Value": float})
    # Pre-format labels to avoid trace misalignment
    pldf["ValueText"] = [fmt.format(v) for v in pldf["Value"].values]

    fig = px.bar(
        pldf,
        x="Value",
        y="Neighbourhood",
        color="Group",
        text="ValueText",
        hover_data={"ValueText": False, "Group": True},
        orientation="h",
        category_orders={"Neighbourhood": pldf["Neighbourhood"].tolist()},
        template="plotly_white",
        color_discrete_map={
            "Veldhuizen A": COL_A,
            "Veldhuizen B": COL_B,
        },
    )
    fig.update_xaxes(title_text=xlabel, zeroline=False, fixedrange=True)
    fig.update_yaxes(title_text="", automargin=True, fixedrange=True)

    # Clean hover
    hover_tmpl = f"%{{y}}<br>{xlabel}: %{{x:.{dec}f}}<extra></extra>"
    fig.update_traces(hovertemplate=hover_tmpl)

    _xmax = float(np.nanmax(pldf["Value"]))
    if np.isfinite(muni_value):
        _xmax = max(_xmax, float(muni_value))
    _pad_factor = 0.15 if show_labels else 0.08
    _xpad = _pad_factor * _xmax if _xmax > 0 else 1.0
    fig.update_xaxes(range=[x_lower, _xmax + _xpad])

    if show_labels:
        fig.update_traces(textposition="outside", cliponaxis=False)
    else:
        fig.update_traces(text=None)

    if np.isfinite(muni_value):
        xavg = float(muni_value)
        fig.add_vline(x=xavg, line_width=2, line_color=COL_AVG)
        fig.add_annotation(
            x=xavg, y=1, xref="x", yref="paper",
            text=f"Ede average: {fmt.format(xavg)}",
            showarrow=False, xanchor="left", yanchor="bottom", xshift=6,
            font=dict(color=COL_AVG),
        )

    fig.update_layout(
        height=height_px,
        margin=dict(l=160, r=180, t=30, b=50), 
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1.0,
            xanchor="left",
            x=1.02,  
            bgcolor="rgba(255,255,255,0.9)",
        ),
        legend_title_text="",
    )

    st.plotly_chart(fig, use_container_width=True, theme=None, config=dict(displayModeBar=False))

    table_df = pldf.rename(columns={"Neighbourhood": "Neighbourhood", "Value": xlabel})
    table_df = table_df[["Neighbourhood", "Group", xlabel]]
    st.dataframe(table_df, use_container_width=True, hide_index=True)

    rendered_interactive = True  
except Exception:
    rendered_interactive = False

# ---------- Static chart fallback ----------
if not rendered_interactive:
    plt.style.use("default")
    row_h     = 0.48
    fig_h     = max(3.6, row_h * n + 1.2) * HEIGHT_SCALE
    left_mar  = min(0.35, 0.08 + 0.012 * max(len(s) for s in names))

    fig, ax = plt.subplots(figsize=(11.5, fig_h), dpi=140)
    ypos = np.arange(n)
    bar_colors = np.where(df["is_A"].to_numpy(), COL_A, COL_B)
    ax.barh(ypos, vals, height=0.62, color=bar_colors)

    ax.set_yticks(ypos)
    ax.set_yticklabels(names)
    ax.invert_yaxis()
    ax.set_xlabel(xlabel)
    ax.set_ylabel("")
    ax.set_xlim(x_lower, x_upper)
    ax.grid(axis="x", linestyle=":", linewidth=0.8, alpha=0.6)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

    if show_labels:
        span = (x_upper - x_lower); thr = 0.15 * span
        for y, v in zip(ypos, vals):
            text = fmt.format(v)
            if v - x_lower > thr:
                ax.text(v - 0.01*span, y, text, va="center", ha="right",
                        color="white", fontsize=9, fontweight="semibold")
            else:
                ax.text(v + 0.01*span, y, text, va="center", ha="left", color="#222", fontsize=9)

    if np.isfinite(muni_value):
        xavg = float(muni_value)
        ax.axvline(x=xavg, color=COL_AVG, linewidth=2)
        ax.text(xavg, -0.7, f"Ede average: {fmt.format(xavg)}",
                color=COL_AVG, ha="left", va="bottom", fontsize=10,
                bbox=dict(facecolor="white", alpha=0.85, edgecolor="none", pad=1.5))

    # Legend for Veldhuizen A/B
    legend_handles = [
        Patch(facecolor=COL_A, edgecolor=COL_A, label="Veldhuizen A"),
        Patch(facecolor=COL_B, edgecolor=COL_B, label="Veldhuizen B"),
    ]
    ax.legend(handles=legend_handles, title="", loc="lower right", frameon=False)

    fig.subplots_adjust(left=left_mar, right=0.97, top=0.92, bottom=0.12)
    st.pyplot(fig)

    # Table
    tbl = df.rename(columns={"LabelName": "Neighbourhood", var_col: xlabel})[
        ["LabelName", "Group", var_col]
    ].rename(columns={"LabelName": "Neighbourhood", var_col: xlabel})
    st.dataframe(tbl, use_container_width=True, hide_index=True)

# ---------- Caption ----------
if np.isfinite(muni_value):
    st.caption(f"Tip: the dark green line marks the Ede municipal average (≈ {fmt.format(float(muni_value))}).")
else:
    st.caption("Tip: the dark green line marks the Ede municipal average.")

# ---------- Collapsible notes ----------
st.divider()
with st.expander("Notes", expanded=False):
    st.markdown(
        """
**What this view demonstrates.** A single indicator (selected from the catalog) is compared across all neighbourhoods in Veldhuizen, with the Ede municipal value shown as a reference line for context. Neighbourhoods are coloured by a simple display grouping: **Veldhuizen A** (De Horsten, De Burgen) versus **Veldhuizen B** (all others). The grouping affects colour and labels only.
"""
    )
