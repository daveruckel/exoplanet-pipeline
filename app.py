import streamlit as st
import duckdb
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Exoplanet Discovery Dashboard",
    page_icon="🪐",
    layout="wide"
)

st.title("🪐 Exoplanet Discovery Dashboard")
st.markdown("Exploring 6,000+ planets discovered beyond our solar system using NASA Exoplanet Archive data.")

# Connect to DuckDB
db_path = "/Users/daveruckel/exoplanet-pipeline/exoplanet_dbt/dev.duckdb"
con = duckdb.connect(db_path, read_only=True)

# Load mart data
df = con.execute("select * from mart_exoplanet_summary").df()
con.close()

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
col1.metric("Total Planets", f"{filtered['planet_count'].sum():,}")
col2.metric("Discovery Methods", filtered["discovery_method"].nunique())
col3.metric("Years Covered", f"{year_range[0]} – {year_range[1]}")
col4.metric("Habitable Zone", f"{filtered['habitable_zone_count'].sum():,}")

st.divider()

# Chart 1 - Discoveries over time
st.subheader("Discoveries Over Time")
by_year = filtered.groupby("discovery_year")["planet_count"].sum().reset_index()
fig1 = px.bar(by_year, x="discovery_year", y="planet_count",
              color_discrete_sequence=["#7B2FBE"],
              labels={"discovery_year": "Year", "planet_count": "Planets Discovered"})
st.plotly_chart(fig1, use_container_width=True)

# Chart 2 - Planet types
st.subheader("Planet Types")
by_type = filtered.groupby("planet_type")["planet_count"].sum().reset_index()
fig2 = px.pie(by_type, names="planet_type", values="planet_count",
              color_discrete_sequence=px.colors.sequential.Purples_r)
st.plotly_chart(fig2, use_container_width=True)

# Chart 3 - Discovery methods
st.subheader("Discovery Methods")
by_method = filtered.groupby("discovery_method")["planet_count"].sum().reset_index().sort_values("planet_count", ascending=True)
fig3 = px.bar(by_method, x="planet_count", y="discovery_method", orientation="h",
              color_discrete_sequence=["#2FB8BE"],
              labels={"planet_count": "Planets", "discovery_method": "Method"})
st.plotly_chart(fig3, use_container_width=True)

# Chart 4 - Top facilities
st.subheader("Top Discovery Facilities")
by_facility = filtered.groupby("discovery_facility")["planet_count"].sum().reset_index().sort_values("planet_count", ascending=False).head(10)
fig4 = px.bar(by_facility, x="planet_count", y="discovery_facility", orientation="h",
              color_discrete_sequence=["#BE2F7B"],
              labels={"planet_count": "Planets", "discovery_facility": "Facility"})
st.plotly_chart(fig4, use_container_width=True)
