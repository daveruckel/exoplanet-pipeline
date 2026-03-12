# 🪐 Exoplanet Discovery Analytics Pipeline

A end-to-end data engineering portfolio project that ingests live NASA exoplanet data, transforms it through a modern dbt pipeline, and serves an interactive analytics dashboard via Streamlit Cloud.

**[🚀 Live Dashboard →](https://daveruckel-exoplanets.streamlit.app)**  
**[💻 GitHub Repository →](https://github.com/daveruckel/exoplanet-pipeline)**

---

## What This Project Does

This pipeline answers the question: *How has humanity's discovery of planets beyond our solar system evolved over time — and what does that reveal about our detection technology?*

It pulls the full NASA Exoplanet Archive catalog (6,100+ confirmed planets), transforms and classifies the data using dbt and DuckDB, then renders it as an interactive dashboard with filters, KPI metrics, and four Plotly visualizations.

---

## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| **Ingestion** | Python + Requests | Fetches live data from NASA TAP API |
| **Storage** | DuckDB | Lightweight analytical database (no server needed) |
| **Transformation** | dbt Core | Staging → intermediate → mart model pattern |
| **Visualization** | Plotly | Interactive charts rendered in-browser |
| **Application** | Streamlit | Dashboard framework and UI |
| **Deployment** | Streamlit Cloud | Free public hosting with live URL |
| **Version Control** | Git + GitHub | Source control and CI/CD trigger |

---

## Pipeline Architecture

```
NASA Exoplanet Archive (TAP API)
            │
            ▼
  Python ingest script
  (scripts/ingest_exoplanets.py)
            │
            ▼
   Raw CSV → DuckDB
  (data/exoplanets_raw.csv)
            │
            ▼
┌─────────────────────────────┐
│        dbt Core             │
│                             │
│  stg_exoplanets             │  ← Clean & rename columns
│         │                   │
│  int_exoplanets_classified  │  ← Add planet_type, habitable_zone flag
│         │                   │
│  mart_exoplanet_summary     │  ← Aggregate by year/method/type/facility
└─────────────────────────────┘
            │
            ▼
   Streamlit App (app.py)
   Live NASA fetch → DuckDB in-memory → Plotly charts
            │
            ▼
   Streamlit Cloud
   daveruckel-exoplanets.streamlit.app
```

---

## dbt Models

### `stg_exoplanets` (Staging)
Reads the raw NASA CSV and applies clean column naming. Filters out rows missing a discovery year.

### `int_exoplanets_classified` (Intermediate)
Adds two derived fields:
- **`planet_type`** — Classifies planets by radius: Rocky, Super-Earth, Sub-Neptune, Neptune-like, Gas Giant
- **`in_habitable_zone`** — Flags planets with equilibrium temperature between 180K–310K

### `mart_exoplanet_summary` (Mart)
Aggregates by discovery year, method, planet type, and facility. Exposes:
- Total planet count per group
- Average radius, mass, and distance
- Habitable zone count per group

---

## Dashboard Features

- **KPI row** — Total planets, discovery methods, year range, habitable zone candidates
- **Discoveries over time** — Bar chart showing the acceleration of exoplanet discovery
- **Planet type breakdown** — Pie chart by classification (Rocky, Gas Giant, etc.)
- **Discovery methods** — Horizontal bar chart (Transit, Radial Velocity, Direct Imaging, etc.)
- **Top discovery facilities** — Which telescopes and missions found the most planets
- **Sidebar filters** — Filter all charts by discovery method and year range

---

## Data Source

**NASA Exoplanet Archive** — Planetary Systems Composite Parameters table (`pscomppars`)  
Public API, no key required.  
Endpoint: `https://exoplanetarchive.ipac.caltech.edu/TAP/sync`

The Streamlit app fetches fresh data on load (cached for 24 hours), so the dashboard always reflects the current confirmed planet catalog.

---

## Local Setup

```bash
# Clone the repo
git clone https://github.com/daveruckel/exoplanet-pipeline.git
cd exoplanet-pipeline

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install dbt-duckdb pandas plotly requests streamlit

# Fetch NASA data
python scripts/ingest_exoplanets.py

# Run dbt transformations
cd exoplanet_dbt
dbt run

# Launch the dashboard
cd ..
streamlit run app.py
```

---

## Project Structure

```
exoplanet-pipeline/
├── app.py                          # Streamlit dashboard (live NASA fetch)
├── requirements.txt                # Streamlit Cloud dependencies
├── scripts/
│   └── ingest_exoplanets.py        # NASA API ingestion script
├── data/
│   └── exoplanets_raw.csv          # Raw data (local only, gitignored)
└── exoplanet_dbt/
    ├── dbt_project.yml
    ├── models/
    │   ├── staging/
    │   │   └── stg_exoplanets.sql
    │   ├── intermediate/
    │   │   └── int_exoplanets_classified.sql
    │   └── marts/
    │       └── mart_exoplanet_summary.sql
    └── profiles.yml (in ~/.dbt/)
```

---

## Author

**Dave Ruckel**  
Program Manager | Data Engineering  
[daveruckel.weebly.com](https://daveruckel.weebly.com)
