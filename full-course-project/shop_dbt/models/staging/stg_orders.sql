select distinct
    order_id,
    customer_id,
    order_date,
    status,
    amount
from read_csv('../data/orders.csv', header = true)