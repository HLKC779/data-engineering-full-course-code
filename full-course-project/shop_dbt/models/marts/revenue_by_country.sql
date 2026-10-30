select
    coalesce(c.country_name, 'Unknown') as country,
    count(*) as orders,
    cast(sum(o.amount) as decimal(10, 2)) as revenue
from {{ ref('stg_orders') }} as o
join {{ ref('stg_customers') }} as cu on cu.customer_id = o.customer_id
left join {{ ref('countries') }} as c on c.code = cu.country_code
where o.status = 'completed'
group by 1
order by revenue desc