"""
National Museums of Kenya — Turkana Basin Fossil Checklist
Interactive specimen portal built with Streamlit + Pandas.

Run:
    streamlit run app.py

Expects 'TurkanaPublicDatabase.csv' in the same directory.
"""

import pandas as pd
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be the first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NMK · Turkana Fossil Checklist",
    page_icon="🦴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# BRAND TOKENS  (derived from NMK logo: near-black bg, sienna tusks, gold spiral)
# ─────────────────────────────────────────────────────────────────────────────
BRAND = {
    "bg_dark":       "#0D0D0D",   # near-black canvas (logo background)
    "bg_panel":      "#161410",   # slightly lifted surface for cards/sidebar
    "bg_card":       "#1E1A16",   # data card / metric tile background
    "sienna":        "#9E4A22",   # primary brand — crossed tusks
    "sienna_light":  "#C4784A",   # hover / active state
    "ivory":         "#F0E0CC",   # tusk highlight, body text
    "ivory_dim":     "#A89880",   # muted text / labels
    "gold":          "#C8A020",   # spiral medallion accent
    "gold_dim":      "#8A6D12",   # subdued gold for dividers
    "rule":          "#2A2420",   # hairline separator colour
}

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
/* ── Reset & base ─────────────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {{
    background-color: {BRAND['bg_dark']} !important;
    color: {BRAND['ivory']} !important;
}}

/* ── Sidebar ───────────────────────────────────────────────────────────── */
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

/* ── Inputs & multiselect ──────────────────────────────────────────────── */
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

/* ── Metric tiles ──────────────────────────────────────────────────────── */
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

/* ── Buttons ───────────────────────────────────────────────────────────── */
.stDownloadButton > button,
.stButton > button {{
    background-color: {BRAND['sienna']} !important;
    color: {BRAND['ivory']} !important;
    border: none !important;
    border-radius: 2px !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-size: 0.75rem !important;
    padding: 0.5rem 1.25rem !important;
    transition: background-color 0.2s ease !important;
}}
.stDownloadButton > button:hover,
.stButton > button:hover {{
    background-color: {BRAND['sienna_light']} !important;
}}

/* ── Dataframe ─────────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {{
    border: 1px solid {BRAND['rule']} !important;
    border-radius: 4px !important;
}}

/* ── Divider ───────────────────────────────────────────────────────────── */
hr {{
    border-color: {BRAND['rule']} !important;
    margin: 0.5rem 0 1.25rem 0 !important;
}}

/* ── Custom header classes ──────────────────────────────────────────────── */
.nmk-wordmark {{
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 0.68rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: {BRAND['ivory_dim']};
    margin: 0;
}}
.nmk-title {{
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 2.0rem;
    font-weight: 400;
    letter-spacing: 0.04em;
    color: {BRAND['ivory']};
    margin: 0.15rem 0 0 0;
    line-height: 1.15;
}}
.nmk-subtitle {{
    font-size: 0.78rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: {BRAND['sienna_light']};
    margin: 0.4rem 0 0 0;
}}
.nmk-gold-rule {{
    height: 1px;
    background: linear-gradient(90deg, {BRAND['gold']}, {BRAND['gold_dim']}, transparent);
    border: none;
    margin: 0.9rem 0 1.4rem 0;
}}
.section-eyebrow {{
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: {BRAND['gold']};
    margin-bottom: 0.2rem;
}}
.record-count {{
    font-size: 0.78rem;
    color: {BRAND['ivory_dim']};
    letter-spacing: 0.06em;
    text-align: right;
    padding-top: 0.35rem;
}}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING & CLEANING
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading specimen records…")
def load_data(path: str = "TurkanaPublicDatabase.csv") -> pd.DataFrame:
    """
    Load and clean the Turkana checklist CSV.

    Key cleaning steps:
    - Integer-like float columns (YearFound, SpecimenNumber, YearPublished, etc.)
      are converted to nullable Int64 first, then to clean strings with no '.0'.
    - All remaining object columns have NaN filled with '' for display.
    - Column names are stripped of accidental whitespace.
    """
    df = pd.read_csv(path, dtype=str, low_memory=False)
    df.columns = df.columns.str.strip()

    # Columns that should display as clean integers (no trailing .0)
    int_like_cols = ["YearFound", "SpecimenNumber", "YearPublished", "RecordNumber"]
    for col in int_like_cols:
        if col in df.columns:
            # coerce to numeric first (handles any stray text), then to Int64, then string
            df[col] = (
                pd.to_numeric(df[col], errors="coerce")
                .astype("Int64")        # pandas nullable integer — preserves NaN
                .astype(str)
                .replace("<NA>", "")   # blank out missing values in display
            )

    # Fill remaining NaN / 'nan' strings with empty string for UI cleanliness
    df = df.fillna("")
    df = df.replace("nan", "", regex=False)

    return df


# ─────────────────────────────────────────────────────────────────────────────
# HELPER: dropdown options (sorted non-blank unique values)
# ─────────────────────────────────────────────────────────────────────────────
def unique_vals(df: pd.DataFrame, col: str) -> list:
    if col not in df.columns:
        return []
    return sorted(v for v in df[col].unique() if v not in ("", None))


# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
try:
    df_raw = load_data()
except FileNotFoundError:
    st.error(
        "**TurkanaPublicDatabase.csv not found.** "
        "Place the CSV file in the same directory as `app.py` and reload."
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
        pass  # logo optional — dashboard functions without it

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

    # ── Taxon filters ────────────────────────────────────────────────────────
    st.markdown(
        f'<p class="section-eyebrow" style="color:{BRAND["sienna_light"]};">Taxonomy</p>',
        unsafe_allow_html=True,
    )

    sel_class = st.multiselect(
        "Class", options=unique_vals(df_raw, "Class"), default=[]
    )
    sel_order = st.multiselect(
        "Order", options=unique_vals(df_raw, "Order"), default=[]
    )
    sel_family = st.multiselect(
        "Family", options=unique_vals(df_raw, "Family"), default=[]
    )
    sel_genus = st.multiselect(
        "Genus", options=unique_vals(df_raw, "Genus"), default=[]
    )

    st.markdown("---")

    # ── Spatiotemporal filters ───────────────────────────────────────────────
    st.markdown(
        f'<p class="section-eyebrow" style="color:{BRAND["sienna_light"]};">Spatiotemporal</p>',
        unsafe_allow_html=True,
    )

    sel_study_area = st.multiselect(
        "Study Area", options=unique_vals(df_raw, "StudyArea"), default=[]
    )
    sel_formation = st.multiselect(
        "Formation", options=unique_vals(df_raw, "Formation"), default=[]
    )

    # YearFound slider — only show if column exists and has numeric values
    year_slider = None
    if "YearFound" in df_raw.columns:
        years_numeric = pd.to_numeric(df_raw["YearFound"], errors="coerce").dropna()
        if not years_numeric.empty:
            y_min, y_max = int(years_numeric.min()), int(years_numeric.max())
            if y_min < y_max:
                year_slider = st.slider(
                    "Year Found",
                    min_value=y_min,
                    max_value=y_max,
                    value=(y_min, y_max),
                )

    st.markdown("---")

    # ── Reset ────────────────────────────────────────────────────────────────
    if st.button("↺  Reset All Filters"):
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# SEARCH BAR  (full-width, above KPIs)
# ─────────────────────────────────────────────────────────────────────────────
search_cols = ["SpecimenNumber", "PartDescription", "PublicationAuthor",
               "Locality", "Species", "Genus"]
search_cols = [c for c in search_cols if c in df_raw.columns]  # keep only present

query = st.text_input(
    label="🔍  Search",
    placeholder="Search by specimen number, part description, author, locality…",
    label_visibility="collapsed",
)


# ─────────────────────────────────────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────────────────────────────────────
df = df_raw.copy()

def apply_multiselect(df: pd.DataFrame, col: str, selection: list) -> pd.DataFrame:
    """Filter dataframe by a multiselect list; no-op if selection is empty."""
    if selection and col in df.columns:
        df = df[df[col].isin(selection)]
    return df

df = apply_multiselect(df, "Class",     sel_class)
df = apply_multiselect(df, "Order",     sel_order)
df = apply_multiselect(df, "Family",    sel_family)
df = apply_multiselect(df, "Genus",     sel_genus)
df = apply_multiselect(df, "StudyArea", sel_study_area)
df = apply_multiselect(df, "Formation", sel_formation)

# Year slider filter
if year_slider is not None and "YearFound" in df.columns:
    y_lo, y_hi = year_slider
    year_numeric = pd.to_numeric(df["YearFound"], errors="coerce")
    df = df[(year_numeric >= y_lo) | (year_numeric.isna())]
    df = df[(pd.to_numeric(df["YearFound"], errors="coerce") <= y_hi) | (pd.to_numeric(df["YearFound"], errors="coerce").isna())]

# Full-text search
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

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_specimens = len(df)
unique_families = df["Family"].nunique() if "Family" in df.columns else 0
unique_genera   = df["Genus"].nunique()  if "Genus"  in df.columns else 0
unique_species  = df["Species"].nunique() if "Species" in df.columns else 0

kpi1.metric("Specimens",       f"{total_specimens:,}")
kpi2.metric("Unique Families", f"{unique_families:,}")
kpi3.metric("Unique Genera",   f"{unique_genera:,}")
kpi4.metric("Unique Species",  f"{unique_species:,}")

st.markdown('<div class="nmk-gold-rule"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# DATA TABLE
# ─────────────────────────────────────────────────────────────────────────────

# Column display order: identifiers first, then taxonomy, then anatomy, then geo
priority_cols = [
    "Museum", "SpecimenPfx", "SpecimenNumber", "SpecimenSfx",
    "YearFound",
    "Class", "Order", "Family", "Genus", "Species",
    "BodyElement", "Side", "PartDescription",
    "StudyArea", "Locality", "Formation", "Member",
    "PublicationAuthor", "YearPublished",
]
display_cols = [c for c in priority_cols if c in df.columns]
remaining    = [c for c in df.columns if c not in display_cols]
display_cols += remaining

df_display = df[display_cols]

# Header row: record count + download button
hdr_left, hdr_right = st.columns([6, 2])
with hdr_left:
    st.markdown(
        f'<p class="section-eyebrow">Specimen Records</p>',
        unsafe_allow_html=True,
    )
with hdr_right:
    csv_bytes = df_display.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇  Download CSV",
        data=csv_bytes,
        file_name="nmk_turkana_filtered.csv",
        mime="text/csv",
        width='stretch',
    )

# Record count tag
st.markdown(
    f'<p class="record-count">{len(df_display):,} record{"s" if len(df_display) != 1 else ""} '
    f'of {len(df_raw):,} total</p>',
    unsafe_allow_html=True,
)

# Render dataframe
st.dataframe(
    df_display,
    width='stretch',
    height=520,
    hide_index=True,
    column_config={
        "SpecimenNumber": st.column_config.TextColumn("Spec. No.", width="small"),
        "YearFound":      st.column_config.TextColumn("Year Found", width="small"),
        "YearPublished":  st.column_config.TextColumn("Yr. Published", width="small"),
        "PartDescription": st.column_config.TextColumn("Part Description", width="large"),
        "PublicationAuthor": st.column_config.TextColumn("Author", width="medium"),
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
    f'Turkana Basin Fossil Checklist ·'
    f'</p>',
    unsafe_allow_html=True,
)
