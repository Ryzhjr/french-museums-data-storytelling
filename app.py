"""One page: a fixed national story, followed by filtered exploration."""

import streamlit as st
from sections.intro import show_intro
from sections.overview import show_overview, show_exploration
from sections.deep_dives import show_deep_dives, show_payments, show_quality
from sections.conclusions import show_conclusions
from utils.io import load_data, load_geojson
from utils.prep import INDICATORS, common_sites, make_tables, payment_comparison, regional_recovery, summarize

st.set_page_config(page_title="French Museums: From Crisis to Recovery", layout="wide")


@st.cache_data(show_spinner=False)
def get_data():
    df_raw = load_data()
    tables = make_tables(df_raw)
    tables["boundaries"] = load_geojson()
    # This national story is prepared before any user filter is applied.
    national = tables["data"]
    tables["timeseries"] = summarize(national, "annee", "total")
    tables["common"] = common_sites(national, "total")
    tables["by_region"] = regional_recovery(tables["common"], sorted(national["region"].unique()))
    tables["payments"] = payment_comparison(national)
    return df_raw, tables


st.title("French Museums: From Crisis to Recovery (2014–2024)")
st.caption("Source: Ministry of Culture - data.gouv.fr - Open Licence")
raw, tables = get_data()

with st.sidebar:
    st.header("Explore filters")
    st.caption("These filters affect Part 2 only. Part 1 is our fixed national analysis.")
    choices = sorted(tables["data"]["region"].unique())
    regions = st.multiselect("Regions / territories", choices, default=choices)
    date_range = st.slider("Year range", 2014, 2024, (2014, 2024))
    metric = st.selectbox("Metric", list(INDICATORS), format_func=lambda name: INDICATORS[name])

st.header("Part 1 - Our Data Story")
show_intro()
show_overview(tables["timeseries"])
show_deep_dives(tables)
show_payments(tables["payments"])
show_conclusions(tables)

st.divider()
st.header("Part 2 - Explore Museum Attendance")
st.caption("Choose regions, years and a metric in the sidebar. The story above does not change.")
df = tables["data"]
filtered = df[df["region"].isin(regions) & df["annee"].between(*date_range)]
show_exploration(filtered, tables["boundaries"], regions, date_range, metric)
show_quality(tables, filtered, metric)
