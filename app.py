"""
National Museums of Kenya — Turkana Basin Fossil Checklist
Interactive specimen portal with geospatial map visualization.

Run:
    streamlit run app.py

Expects 'TurkanaPublicDatabase.csv' in the same directory.
Optionally place 'museumslogo.png' in the same directory for the header logo.

Dependencies:
    pip install streamlit pandas pydeck
"""

import pandas as pd
import pydeck as pdk
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NMK · Turkana Fossil Checklist",
    page_icon="🦴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# BRAND TOKENS  (extracted from NMK logo)
# ─────────────────────────────────────────────────────────────────────────────
BRAND = {
    "bg_dark":      "#0D0D0D",
    "bg_panel":     "#161410",
    "bg_card":      "#1E1A16",
    "sienna":       "#9E4A22",
    "sienna_light": "#C4784A",
    "ivory":        "#F0E0CC",
    "ivory_dim":    "#A89880",
    "gold":         "#C8A020",
    "gold_dim":     "#8A6D12",
    "rule":         "#2A2420",
}

# ─────────────────────────────────────────────────────────────────────────────
# LOCALITY → COORDINATES LOOKUP
# Curated from published literature for all major Turkana Basin fossil sites.
# Coordinates sourced from Wikipedia, TBI, and peer-reviewed publications.
# ─────────────────────────────────────────────────────────────────────────────
LOCALITY_COORDS = {
    # ── East Turkana / Koobi Fora region ────────────────────────────────────
    "Koobi Fora":       (3.968,  36.176),
    "Koobi Fora Ridge": (3.968,  36.176),
    "East Turkana":     (3.800,  36.200),
    "Ileret":           (4.312,  36.227),
    "Allia Bay":        (3.584,  36.268),
    "Area 1":           (3.900,  36.190),
    "Area 4":           (3.870,  36.175),
    "Area 6A":          (3.840,  36.170),
    "Area 7":           (3.860,  36.160),
    "Area 8A":          (3.870,  36.155),
    "Area 10":          (3.885,  36.145),
    "Area 11":          (3.895,  36.140),
    "Area 12":          (3.910,  36.148),
    "Area 13":          (3.930,  36.155),
    "Area 101":         (3.840,  36.180),
    "Area 102":         (3.845,  36.185),
    "Area 103":         (3.850,  36.190),
    "Area 104":         (3.855,  36.195),
    "Area 105":         (3.858,  36.200),
    "Area 110":         (3.870,  36.205),
    "Area 115":         (3.900,  36.210),
    "Area 116":         (3.905,  36.215),
    "Area 130":         (3.940,  36.200),
    "Area 131":         (3.945,  36.205),
    # ── West Turkana / Nachukui Formation ───────────────────────────────────
    "Nariokotome":      (4.128,  35.788),
    "West Turkana":     (3.800,  35.800),
    "Nachukui":         (3.700,  35.780),
    "Lothagam":         (2.927,  36.046),
    "Kanapoi":          (2.350,  36.065),
    "Lomekwi":          (3.530,  35.747),
    "Kalochoro":        (3.555,  35.752),
    "Kokiselei":        (3.567,  35.758),
    "Natoo":            (3.480,  35.740),
    "Nakwai":           (3.460,  35.735),
    "Kataboi":          (3.625,  35.762),
    "Murua Rith":       (3.750,  35.790),
    "Labur":            (3.720,  35.810),
    "Naiyena Engol":    (3.590,  35.768),
    # ── North / Omo Valley ──────────────────────────────────────────────────
    "Omo":              (4.800,  35.950),
    "Omo Valley":       (4.800,  35.950),
    "Shungura":         (4.850,  35.970),
    "Sibiloi":          (3.961,  36.342),
    "Sibiloi NP":       (3.961,  36.342),
    # ── South & miscellaneous ───────────────────────────────────────────────
    "Chesowanja":       (0.322,  36.212),
    "Baringo":          (0.477,  36.011),
    "Samburu":          (1.074,  37.033),
    "Turkwel":          (3.100,  35.850),
    "Kerio":            (2.800,  35.980),
    "Lokone":           (2.600,  35.700),
    "Muruarot":         (3.400,  35.820),
}

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {{
    background-color: {BRAND['bg_dark']} !important;
    color: {BRAND['ivory']} !important;
}}
[data-testid="stSidebar"] {{
    background-color: {BRAND['bg_panel']} !important;
    border-right: 1px solid {BRAND['rule']} !important;
}}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {{
    color: {BRAND['ivory_dim']} !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {{
    background-color: {BRAND['sienna']} !important;
    color: {BRAND['ivory']} !important;
}}
[data-baseweb="input"] input,
[data-baseweb="select"] div,
[data-baseweb="textarea"] textarea {{
    background-color: {BRAND['bg_card']} !important;
    color: {BRAND['ivory']} !important;
    border-color: {BRAND['rule']} !important;
}}
[data-baseweb="menu"] {{
    background-color: {BRAND['bg_card']} !important;
}}
[data-baseweb="option"]:hover {{
    background-color: {BRAND['sienna']} !important;
}}
[data-testid="stMetric"] {{
    background-color: {BRAND['bg_card']} !important;
    border: 1px solid {BRAND['rule']} !important;
    border-top: 2px solid {BRAND['sienna']} !important;
    border-radius: 4px !important;
    padding: 1rem 1.25rem !important;
}}
[data-testid="stMetricLabel"] {{
    color: {BRAND['ivory_dim']} !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}}
[data-testid="stMetricValue"] {{
    color: {BRAND['ivory']} !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
}}
.stDownloadButton > button, .stButton > button {{
    background-color: {BRAND['sienna']} !important;
    color: {BRAND['ivory']} !important;
    border: none !important;
    border-radius: 2px !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-size: 0.75rem !important;
    padding: 0.5rem 1.25rem !important;
}}
.stDownloadButton > button:hover, .stButton > button:hover {{
    background-color: {BRAND['sienna_light']} !important;
}}
[data-testid="stDataFrame"] {{
    border: 1px solid {BRAND['rule']} !important;
    border-radius: 4px !important;
}}
hr {{ border-color: {BRAND['rule']} !important; margin: 0.5rem 0 1.25rem 0 !important; }}
.nmk-wordmark {{
    font-family: 'Georgia', serif;
    font-size: 0.68rem; letter-spacing: 0.22em;
    text-transform: uppercase; color: {BRAND['ivory_dim']}; margin: 0;
}}
.nmk-title {{
    font-family: 'Georgia', serif;
    font-size: 2.0rem; font-weight: 400; letter-spacing: 0.04em;
    color: {BRAND['ivory']}; margin: 0.15rem 0 0 0; line-height: 1.15;
}}
.nmk-subtitle {{
    font-size: 0.78rem; letter-spacing: 0.14em;
    text-transform: uppercase; color: {BRAND['sienna_light']}; margin: 0.4rem 0 0 0;
}}
.nmk-gold-rule {{
    height: 1px;
    background: linear-gradient(90deg, {BRAND['gold']}, {BRAND['gold_dim']}, transparent);
    border: none; margin: 0.9rem 0 1.4rem 0;
}}
.section-eyebrow {{
    font-size: 0.65rem; letter-spacing: 0.18em;
    text-transform: uppercase; color: {BRAND['gold']}; margin-bottom: 0.2rem;
}}
.record-count {{
    font-size: 0.78rem; color: {BRAND['ivory_dim']};
    letter-spacing: 0.06em; text-align: right; padding-top: 0.35rem;
}}
/* Map tooltip override */
.deck-tooltip {{
    background: {BRAND['bg_card']} !important;
    color: {BRAND['ivory']} !important;
    border: 1px solid {BRAND['sienna']} !important;
    border-radius: 4px !important;
    font-family: 'Georgia', serif !important;
    font-size: 0.82rem !important;
}}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING & CLEANING
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading specimen records…")
def load_data(path: str = "TurkanaPublicDatabase.csv") -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str, low_memory=False)
    df.columns = df.columns.str.strip()

    int_like_cols = ["YearFound", "SpecimenNumber", "YearPublished", "RecordNumber"]
    for col in int_like_cols:
        if col in df.columns:
            df[col] = (
                pd.to_numeric(df[col], errors="coerce")
                .astype("Int64")
                .astype(str)
                .replace("<NA>", "")
            )

    df = df.fillna("").replace("nan", "", regex=False)
    return df


def unique_vals(df: pd.DataFrame, col: str) -> list:
    if col not in df.columns:
        return []
    return sorted(v for v in df[col].unique() if v not in ("", None))


# ─────────────────────────────────────────────────────────────────────────────
# MAP DATA BUILDER
# ─────────────────────────────────────────────────────────────────────────────
def build_map_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Geocode each record using the Locality column against the curated
    LOCALITY_COORDS lookup.  Returns a DataFrame with lat/lon columns
    plus aggregated specimen counts per site, ready for pydeck layers.

    Matching strategy:
    1. Exact match against known locality names (case-insensitive).
    2. Partial / 'starts-with' match for area codes like "Area 6A".
    3. StudyArea fallback if Locality is blank or unmatched.
    """
    loc_col = "Locality" if "Locality" in df.columns else None
    area_col = "StudyArea" if "StudyArea" in df.columns else None

    # Normalise lookup keys to lower-case for matching
    coords_lower = {k.lower(): v for k, v in LOCALITY_COORDS.items()}

    rows = []
    for _, row in df.iterrows():
        lat, lon = None, None
        loc_name = ""

        # 1. Try Locality
        if loc_col:
            raw = str(row.get(loc_col, "")).strip()
            if raw:
                key = raw.lower()
                if key in coords_lower:
                    lat, lon = coords_lower[key]
                    loc_name = raw
                else:
                    # partial prefix match (e.g. "Area 6A West" → "Area 6A")
                    for k, v in coords_lower.items():
                        if key.startswith(k) or k.startswith(key):
                            lat, lon = v
                            loc_name = raw
                            break

        # 2. Fallback to StudyArea
        if lat is None and area_col:
            raw = str(row.get(area_col, "")).strip()
            if raw:
                key = raw.lower()
                if key in coords_lower:
                    lat, lon = coords_lower[key]
                    loc_name = raw
                else:
                    for k, v in coords_lower.items():
                        if key.startswith(k) or k.startswith(key):
                            lat, lon = v
                            loc_name = raw
                            break

        if lat is not None:
            rows.append({
                "lat": lat,
                "lon": lon,
                "locality": loc_name or "Unknown",
                "family": row.get("Family", ""),
                "genus": row.get("Genus", ""),
                "species": row.get("Species", ""),
                "specimen": row.get("SpecimenNumber", ""),
                "year": row.get("YearFound", ""),
                "formation": row.get("Formation", ""),
            })

    if not rows:
        return pd.DataFrame()

    geo_df = pd.DataFrame(rows)

    # Aggregate: count per (locality, lat, lon) for bubble sizing
    agg = (
        geo_df.groupby(["locality", "lat", "lon"])
        .agg(
            count=("specimen", "count"),
            families=("family", lambda x: len(set(v for v in x if v))),
            genera=("genus", lambda x: len(set(v for v in x if v))),
            sample_genus=("genus", lambda x: next((v for v in x if v), "—")),
            sample_formation=("formation", lambda x: next((v for v in x if v), "—")),
        )
        .reset_index()
    )

    # Radius scaled by sqrt(count) so large sites don't dominate visually
    import math
    agg["radius"] = agg["count"].apply(lambda n: max(1500, int(math.sqrt(n) * 1200)))

    # Tooltip HTML
    agg["tooltip"] = agg.apply(
        lambda r: (
            f"<b>{r['locality']}</b><br/>"
            f"Specimens: <b>{r['count']:,}</b><br/>"
            f"Families: {r['families']} · Genera: {r['genera']}<br/>"
            f"Formation: {r['sample_formation']}"
        ),
        axis=1,
    )
    return agg


# ─────────────────────────────────────────────────────────────────────────────
# LOAD
# ─────────────────────────────────────────────────────────────────────────────
try:
    df_raw = load_data()
except FileNotFoundError:
    st.error(
        "**TurkanaPublicDatabase.csv not found.** "
        "Place the CSV in the same directory as `app.py` and reload."
    )
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
col_logo, col_title = st.columns([1, 9], gap="medium")
with col_logo:
    try:
        st.image("museumslogo.png", width=90)
    except Exception:
        pass
with col_title:
    st.markdown('<p class="nmk-wordmark">National Museums of Kenya</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="nmk-title">Turkana Basin Fossil Checklist</h1>', unsafe_allow_html=True)
    st.markdown('<p class="nmk-subtitle">Where Heritage Lives On · Specimen Database Portal</p>', unsafe_allow_html=True)

st.markdown('<div class="nmk-gold-rule"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — FILTERS
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f'<p style="color:{BRAND["gold"]};font-size:0.7rem;letter-spacing:0.18em;'
        f'text-transform:uppercase;margin-bottom:0.8rem;">Filter Specimens</p>',
        unsafe_allow_html=True,
    )

    st.markdown(f'<p class="section-eyebrow" style="color:{BRAND["sienna_light"]};">Taxonomy</p>', unsafe_allow_html=True)
    sel_class  = st.multiselect("Class",  options=unique_vals(df_raw, "Class"),  default=[])
    sel_order  = st.multiselect("Order",  options=unique_vals(df_raw, "Order"),  default=[])
    sel_family = st.multiselect("Family", options=unique_vals(df_raw, "Family"), default=[])
    sel_genus  = st.multiselect("Genus",  options=unique_vals(df_raw, "Genus"),  default=[])

    st.markdown("---")
    st.markdown(f'<p class="section-eyebrow" style="color:{BRAND["sienna_light"]};">Spatiotemporal</p>', unsafe_allow_html=True)
    sel_study_area = st.multiselect("Study Area", options=unique_vals(df_raw, "StudyArea"),  default=[])
    sel_formation  = st.multiselect("Formation",  options=unique_vals(df_raw, "Formation"),  default=[])

    year_slider = None
    if "YearFound" in df_raw.columns:
        years_numeric = pd.to_numeric(df_raw["YearFound"], errors="coerce").dropna()
        if not years_numeric.empty:
            y_min, y_max = int(years_numeric.min()), int(years_numeric.max())
            if y_min < y_max:
                year_slider = st.slider("Year Found", min_value=y_min, max_value=y_max, value=(y_min, y_max))

    st.markdown("---")
    if st.button("↺  Reset All Filters"):
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# SEARCH BAR
# ─────────────────────────────────────────────────────────────────────────────
search_cols = [c for c in ["SpecimenNumber", "PartDescription", "PublicationAuthor",
                            "Locality", "Species", "Genus"] if c in df_raw.columns]
query = st.text_input(
    label="🔍  Search",
    placeholder="Search by specimen number, part description, author, locality…",
    label_visibility="collapsed",
)


# ─────────────────────────────────────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────────────────────────────────────
def apply_multiselect(df, col, sel):
    return df[df[col].isin(sel)] if sel and col in df.columns else df

df = df_raw.copy()
df = apply_multiselect(df, "Class",     sel_class)
df = apply_multiselect(df, "Order",     sel_order)
df = apply_multiselect(df, "Family",    sel_family)
df = apply_multiselect(df, "Genus",     sel_genus)
df = apply_multiselect(df, "StudyArea", sel_study_area)
df = apply_multiselect(df, "Formation", sel_formation)

if year_slider is not None and "YearFound" in df.columns:
    y_lo, y_hi = year_slider
    ynum = pd.to_numeric(df["YearFound"], errors="coerce")
    df = df[ynum.isna() | ((ynum >= y_lo) & (ynum <= y_hi))]

if query.strip():
    q = query.strip().lower()
    mask = pd.Series(False, index=df.index)
    for col in search_cols:
        mask |= df[col].str.lower().str.contains(q, na=False)
    df = df[mask]


# ─────────────────────────────────────────────────────────────────────────────
# KPI METRICS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-eyebrow">Overview</p>', unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)
k1.metric("Specimens",       f"{len(df):,}")
k2.metric("Unique Families", f"{df['Family'].nunique() if 'Family' in df.columns else 0:,}")
k3.metric("Unique Genera",   f"{df['Genus'].nunique()  if 'Genus'  in df.columns else 0:,}")
k4.metric("Unique Species",  f"{df['Species'].nunique() if 'Species' in df.columns else 0:,}")

st.markdown('<div class="nmk-gold-rule"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# MAP  —  PyDeck scatterplot / bubble map (Gradient & Granular Legend)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-eyebrow">Fossil Recovery Sites</p>', unsafe_allow_html=True)

map_df = build_map_df(df)
mapped_count = map_df["count"].sum() if not map_df.empty else 0
unmapped_count = len(df) - mapped_count

# Info strip
map_info_l, map_info_r = st.columns([7, 3])
with map_info_l:
    if not map_df.empty:
        st.caption(
            f"Showing **{len(map_df)} sites** · "
            f"**{int(mapped_count):,}** specimens geocoded · "
            f"{int(unmapped_count):,} without mapped coordinates"
        )
    else:
        st.caption("No geocodable locality data for the current filter selection.")

if not map_df.empty:
# 1. Monochromatic Saturation Gradient (Base: Green Palette)
    def assign_intensity_color(count):
        if count <= 10:
            return [115, 130, 115]    # Faint, highly desaturated slate-green
        elif count <= 100:
            return [85, 145, 95]      # Muted light green
        elif count <= 1000:
            return [50, 165, 70]      # Medium-saturation standard green
        elif count <= 2500:
            return [20, 190, 50]      # High-saturation rich green
        else:
            return [0, 225, 40]       # Max-intensity blazing green hotspot

    # Map colors to dataset
    map_df["color_rgb"] = map_df["count"].apply(assign_intensity_color)

    # 2. Configure scatter layers with fixed radius footprints
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position="[lon, lat]",
        get_radius=2200,                         # Uniform size to enforce focus on color intensity
        get_fill_color="color_rgb",              # Dynamic gradient assignment
        get_line_color=[13, 15, 20, 220],        # Crisp dark outline to split overlapping circles
        stroked=True,
        filled=True,
        radius_min_pixels=6,
        radius_max_pixels=20,
        line_width_min_pixels=1,
        pickable=True,
        auto_highlight=True,
        highlight_color=[240, 224, 204, 120],
    )

    # Text labels for the top-15 densest sites
    top_sites = map_df.nlargest(15, "count").copy()
    text_layer = pdk.Layer(
        "TextLayer",
        data=top_sites,
        get_position="[lon, lat]",
        get_text="locality",
        get_size=11,
        get_color=[240, 224, 204, 190],
        get_alignment_baseline="'bottom'",
        get_pixel_offset=[0, -10],
        pickable=False,
    )

    view = pdk.ViewState(
        latitude=map_df["lat"].mean(),
        longitude=map_df["lon"].mean(),
        zoom=6.4,
        pitch=20,
        bearing=0,
    )

    deck = pdk.Deck(
        layers=[scatter_layer, text_layer],
        initial_view_state=view,
        map_style="dark",
        tooltip={
            "html": "{tooltip}",
            "style": {
                "backgroundColor": "#1E1A16",
                "color": "#F0E0CC",
                "border": "1px solid #9E4A22",
                "borderRadius": "4px",
                "fontFamily": "Georgia, serif",
                "fontSize": "13px",
                "padding": "8px 12px",
            },
        },
    )

    # Render interactive PyDeck workspace
    st.pydeck_chart(deck, width='stretch', height=480)

   # 3. High-Contrast Monochromatic Green Legend UI
    st.markdown(
        """
        <div style="display: flex; flex-wrap: wrap; gap: 1.25rem; justify-content: flex-start; align-items: center; margin-top: -10px; padding: 0.6rem 1.2rem; background: #161410; border-radius: 4px; border: 1px solid #2A2420;">
            <span style="font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: #A89880;">Specimen Density:</span>
            <div style="display: flex; align-items: center; gap: 0.45rem; font-size: 0.8rem; color: #F0E0CC;">
                <span style="display: inline-block; width: 11px; height: 11px; border-radius: 50%; background: rgb(115, 130, 115); box-shadow: inset 0 0 0 1px rgba(0,0,0,0.2);"></span> 1 – 10 (Faint)
            </div>
            <div style="display: flex; align-items: center; gap: 0.45rem; font-size: 0.8rem; color: #F0E0CC;">
                <span style="display: inline-block; width: 11px; height: 11px; border-radius: 50%; background: rgb(85, 145, 95); box-shadow: inset 0 0 0 1px rgba(0,0,0,0.2);"></span> 11 – 100
            </div>
            <div style="display: flex; align-items: center; gap: 0.45rem; font-size: 0.8rem; color: #F0E0CC;">
                <span style="display: inline-block; width: 11px; height: 11px; border-radius: 50%; background: rgb(50, 165, 70); box-shadow: inset 0 0 0 1px rgba(0,0,0,0.2);"></span> 101 – 1,000
            </div>
            <div style="display: flex; align-items: center; gap: 0.45rem; font-size: 0.8rem; color: #F0E0CC;">
                <span style="display: inline-block; width: 11px; height: 11px; border-radius: 50%; background: rgb(20, 190, 50); box-shadow: inset 0 0 0 1px rgba(0,0,0,0.2);"></span> 1,001 – 2,500
            </div>
            <div style="display: flex; align-items: center; gap: 0.45rem; font-size: 0.8rem; color: #F0E0CC;">
                <span style="display: inline-block; width: 11px; height: 11px; border-radius: 50%; background: rgb(0, 225, 40); box-shadow: inset 0 0 0 1px rgba(0,0,0,0.2);"></span> 2,501 – 4,000+ (Dense)
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Compact legend
    leg_cols = st.columns(3)
    with leg_cols[0]:
        st.markdown(
            f'<span style="display:inline-block;width:12px;height:12px;border-radius:50%;'
            f'background:{BRAND["sienna"]};margin-right:6px;"></span>'
            f'<span style="font-size:0.72rem;color:{BRAND["ivory_dim"]};'
            f'letter-spacing:0.07em;">Fossil recovery site</span>',
            unsafe_allow_html=True,
        )
    with leg_cols[1]:
        st.markdown(
            f'<span style="font-size:0.72rem;color:{BRAND["ivory_dim"]};'
            f'letter-spacing:0.07em;">Bubble size ∝ √(specimen count)</span>',
            unsafe_allow_html=True,
        )
    with leg_cols[2]:
        st.markdown(
            f'<span style="font-size:0.72rem;color:{BRAND["ivory_dim"]};'
            f'letter-spacing:0.07em;">Labels = top 15 sites by count</span>',
            unsafe_allow_html=True,
        )

else:
    st.info("Adjust your filters to see sites on the map.")

st.markdown('<div class="nmk-gold-rule"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# DATA TABLE
# ─────────────────────────────────────────────────────────────────────────────
priority_cols = [
    "Museum", "SpecimenPfx", "SpecimenNumber", "SpecimenSfx", "YearFound",
    "Class", "Order", "Family", "Genus", "Species",
    "BodyElement", "Side", "PartDescription",
    "StudyArea", "Locality", "Formation", "Member",
    "PublicationAuthor", "YearPublished",
]
display_cols = [c for c in priority_cols if c in df.columns]
display_cols += [c for c in df.columns if c not in display_cols]
df_display = df[display_cols]

hdr_l, hdr_r = st.columns([6, 2])
with hdr_l:
    st.markdown('<p class="section-eyebrow">Specimen Records</p>', unsafe_allow_html=True)
with hdr_r:
    st.download_button(
        label="⬇  Download CSV",
        data=df_display.to_csv(index=False).encode("utf-8"),
        file_name="nmk_turkana_filtered.csv",
        mime="text/csv",
        width='stretch',
    )

st.markdown(
    f'<p class="record-count">{len(df_display):,} record{"s" if len(df_display) != 1 else ""} '
    f'of {len(df_raw):,} total</p>',
    unsafe_allow_html=True,
)

st.dataframe(
    df_display,
    width='stretch',
    height=480,
    hide_index=True,
    column_config={
        "SpecimenNumber":    st.column_config.TextColumn("Spec. No.",       width="small"),
        "YearFound":         st.column_config.TextColumn("Year Found",      width="small"),
        "YearPublished":     st.column_config.TextColumn("Yr. Published",   width="small"),
        "PartDescription":   st.column_config.TextColumn("Part Description",width="large"),
        "PublicationAuthor": st.column_config.TextColumn("Author",          width="medium"),
    },
)


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    f'<p style="font-size:0.68rem;letter-spacing:0.1em;color:{BRAND["ivory_dim"]};'
    f'text-align:center;text-transform:uppercase;">'
    f'National Museums of Kenya · Palaeontology Department · '
    f'Turkana Basin Fossil Checklist · Proof of Concept Portal'
    f'</p>',
    unsafe_allow_html=True,
)