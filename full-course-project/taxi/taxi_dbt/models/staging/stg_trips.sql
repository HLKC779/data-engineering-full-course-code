select
    tpep_pickup_datetime as pickup_at,
    tpep_dropoff_datetime as dropoff_at,
    PULocationID as pickup_zone_id,
    DOLocationID as dropoff_zone_id,
    payment_type,
    trip_distance,
    fare_amount,
    tip_amount,
    total_amount
from {{ source('raw', 'raw_trips') }}
where tpep_pickup_datetime >= '2024-01-01'
    and tpep_pickup_datetime < '2024-03-01'
    and tpep_dropoff_datetime > tpep_pickup_datetime
    and tpep_dropoff_datetime < tpep_pickup_datetime + interval 1 day
    and trip_distance > 0
    and total_amount > 0