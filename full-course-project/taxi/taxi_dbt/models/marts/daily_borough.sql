select
    pickup_date,
    pickup_borough,
    count(*) as trips,
    round(sum(total_amount), 2) as revenue,
    round(avg(duration_min), 1) as avg_minutes
from {{ ref('fct_trips') }}
group by all