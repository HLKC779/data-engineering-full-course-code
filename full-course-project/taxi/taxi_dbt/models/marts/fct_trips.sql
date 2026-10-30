select
    t.*,
    cast(t.pickup_at as date) as pickup_date,
    hour(t.pickup_at) as pickup_hour,
    date_diff('minute', t.pickup_at, t.dropoff_at) as duration_min,
    z.borough as pickup_borough,
    z.zone_name as pickup_zone
from {{ ref('stg_trips') }} as t
left join {{ ref('stg_zones') }} as z on z.zone_id = t.pickup_zone_id