import sys
import importlib.metadata as md

python_version = sys.version.split()[0]
print("Python", python_version)
issues = []
if sys.version_info[:2] != (3, 13):
    issues.append(f"Use Python 3.13.x; found {python_version}")

packages = [
    "pandas",
    "polars",
    "duckdb",
    "pyarrow",
    "psycopg",
    "pyspark",
    "dbt-core",
    "dbt-duckdb",
    "confluent-kafka",
    "pytest",
    "requests",
]
missing = []

for pkg in packages:
    try:
        version = md.version(pkg)
    except md.PackageNotFoundError:
        version = "MISSING"
        missing.append(pkg)
    print(f"{pkg:16} {version}")

if missing:
    issues.append(f"Missing packages: {', '.join(missing)}")

if issues:
    print("\nSetup issues:")
    for issue in issues:
        print(f"- {issue}")
    if missing:
        print("Install packages with: uv pip install -r requirements.txt")
    if sys.version_info[:2] != (3, 13):
        print("Create the expected environment with: uv venv .venv-data-engineering --python 3.13")
    sys.exit(1)