set -e
python make_data.py "${1:-16}"
python incremental.py
python etl.py
python aggregates.py
python report.py
echo "pipeline finished"