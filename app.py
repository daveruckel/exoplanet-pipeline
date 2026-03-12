import streamlit as st
import duckdb
import plotly.express as px
import pandas as pd
import requests
from io import StringIO

st.set_page_config(
    page_title="Exoplanet Discovery Dashboard",
    page_icon="🪐",
    layout="wide"
)

st.title("🪐 Exoplanet Discovery Dashboard")
st.markdown("Exploring 6,000+ planets discovered beyond our solar system — live data from NASA Exoplanet Archive.")

@st.cache_data(ttl=86400)
def load_data():
    url = (
        "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
        "?query=select+pl_name,hostname,disc_year,discoverymethod,"
        "pl_rade,pl_masse,pl_orbper,pl_eqt,sy_dist,disc_facility"
        "+from+pscomppars"
        "&format=csv"
    )
    response = requests.get(url, timeout=60)
    df = pd.read_csv(StringIO(response.text))
    df = df[df["disc_year"].notna()]

    con = duckdb.connect()
    con.register("raw", df)
    result = con.execute("""
        select
            pl_name                 as planet_name,
            hostname                as host_star,
            disc_year               as discovery_year,
            discoverymethod         as discovery_method,
            pl_rade                 as planet_radius_earth,
            pl_masse                as planet_mass_earth,
            pl_orbper               as orbital_period_days,
            pl_eqt                  as equilibrium_temp_k,
            sy_dist                 as distance_light_years,
            disc_facility           as discovery_facility,
            case
                when pl_rade < 1.25  then 'Rocky'
                when pl_rade < 2.0   then 'Super-Earth'
                when pl_rade < 4.0   then 'Sub-Neptune'
                when pl_rade < 10.0  then 'Neptune-like'
                else                      'Gas Giant'
            end as planet_type,
            case
                when pl_eqt between 180 and 310 then true
                else false
            end as in_habitable_zone
        from raw
    """).df()
    con.close()
    return result

with st.spinner("Loading live data from NASA..."):
    df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
methods = ["All"] + sorted(df["discovery_method"].dropna().unique().tolist())
selected_method = st.sidebar.selectbox("Discovery Method", methods)

min_year = int(df["discovery_year"].min())
max_year = int(df["discovery_year"].max())
year_range = st.sidebar.slider("Discovery Year", min_year, max_year, (min_year, max_year))

# Apply filters
filtered = df[
    (df["discovery_year"] >= year_range[0]) &
    (df["discovery_year"] <= year_range[1])
]
if selected_method != "All":
    filtered = filtered[filtered["discovery_method"] == selected_method]

# KPI row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Planets", f"{len(filtered):,}")
col2.metric("Discovery Methods", filtered["discovery_method"].nunique())
col3.metric("Years Covered", f"{year_range[0]} – {year_range[1]}")
col4.metric("Habitable Zone", f"{filtered['in_habitable_zone'].sum():,}")

st.divider()

# Chart 1 - Discoveries over time
st.subheader("Discoveries Over Time")
by_year = filtered.groupby("discovery_year").size().reset_index(name="planet_count")
fig1 = px.bar(by_year, x="discovery_year", y="planet_count",
              color_discrete_sequence=["#7B2FBE"],
              labels={"discovery_year": "Year", "planet_count": "Planets Discovered"})
st.plotly_chart(fig1, use_container_width=True)

# Chart 2 - Planet types
st.subheader("Planet Types")
by_type = filtered["planet_type"].value_counts().reset_index()
by_type.columns = ["planet_type", "count"]
fig2 = px.pie(by_type, names="planet_type", values="count",
              color_discrete_sequence=px.colors.sequential.Purples_r)
st.plotly_chart(fig2, use_container_width=True)

# Chart 3 - Discovery methods
st.subheader("Discovery Methods")
by_method = filtered["discovery_method"].value_counts().reset_index()
by_method.columns = ["discovery_method", "count"]
by_method = by_method.sort_values("count")
fig3 = px.bar(by_method, x="count", y="discovery_method", orientation="h",
              color_discrete_sequence=["#2FB8BE"],
              labels={"count": "Planets", "discovery_method": "Method"})
st.plotly_chart(fig3, use_container_width=True)

# Chart 4 - Top facilities
st.subheader("Top Discovery Facilities")
by_facility = filtered["discovery_facility"].value_counts().head(10).reset_index()
by_facility.columns = ["discovery_facility", "count"]
by_facility = by_facility.sort_values("count")
fig4 = px.bar(by_facility, x="count", y="discovery_facility", orientation="h",
              color_discrete_sequence=["#BE2F7B"],
              labels={"count": "Planets", "discovery_facility": "Facility"})
st.plotly_chart(fig4, use_container_width=True)
