with classified as (
    select * from {{ ref('int_exoplanets_classified') }}
),

summary as (
    select
        discovery_year,
        discovery_method,
        planet_type,
        discovery_facility,
        count(*)                                    as planet_count,
        round(avg(planet_radius_earth), 2)          as avg_radius_earth,
        round(avg(planet_mass_earth), 2)            as avg_mass_earth,
        round(avg(distance_light_years), 2)         as avg_distance_ly,
        sum(case when in_habitable_zone then 1
            else 0 end)                             as habitable_zone_count
    from classified
    group by
        discovery_year,
        discovery_method,
        planet_type,
        discovery_facility
)

select * from summary
