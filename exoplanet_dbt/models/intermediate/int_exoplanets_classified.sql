with staging as (
    select * from {{ ref('stg_exoplanets') }}
),

classified as (
    select
        *,
        case
            when planet_radius_earth < 1.25                then 'Rocky'
            when planet_radius_earth < 2.0                 then 'Super-Earth'
            when planet_radius_earth < 4.0                 then 'Sub-Neptune'
            when planet_radius_earth < 10.0                then 'Neptune-like'
            else                                                'Gas Giant'
        end as planet_type,

        case
            when equilibrium_temp_k between 180 and 310    then true
            else                                                false
        end as in_habitable_zone

    from staging
)

select * from classified
