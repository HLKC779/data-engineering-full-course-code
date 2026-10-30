select
    customer_id,
    name,
    lower(trim(email)) as email,
    country as country_code,
    signup_date
from read_csv('../data/customers.csv', header = true)