with source as (
    select * from read_csv_auto('/Users/daveruckel/exoplanet-pipeline/data/exoplanets_raw.csv')
),

renamed as (
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
        disc_facility           as discovery_facility
    from source
    where disc_year is not null
)

select * from renamed
