select *
from {{ ref('fct_trips') }}
where duration_min > 24 * 60