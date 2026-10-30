Data Engineering Full Course for Beginners (4.5 Hours) - SQL, Python, PostgreSQL, dbt, Airflow, Spark, Kafka
Course source code - PyInns (pyinns.com)

Watch the video: [YOUTUBE_LINK_PLACEHOLDER]

WHAT'S INSIDE
Python ETL scripts, SQL lessons (sql/), two dbt projects (shop_dbt, taxi/taxi_dbt),
Airflow DAGs, Kafka producer/consumer, PySpark, pytest tests, and the synthetic
'Bean & Leaf' shop dataset (data/). Copy pg.env.example and airflow.env.example
to pg.env and airflow.env for local settings; those local files are not tracked.
The NYC taxi data is NOT included - taxi/download.py fetches it from NYC TLC.

HOW TO RUN
Full step-by-step instructions are in HOW_TO_RUN.txt. Short version:
  uv venv .venv-data-engineering --python 3.13
  source .venv-data-engineering/bin/activate && uv pip install -r requirements.txt
  python check_setup.py
  python taxi/download.py 2024-01 2024-02   (downloads the taxi data)
Linux/macOS, or WSL on Windows (Airflow needs it).

LICENCE
Code: MIT licence, copyright PyInns (see LICENSE).
Data: data/ is synthetic, made for this course. NYC taxi data comes from the NYC Taxi &
Limousine Commission under NYC Open Data terms and is downloaded by you, not shipped.

This is free learning code shared with the video. It is not production code.
