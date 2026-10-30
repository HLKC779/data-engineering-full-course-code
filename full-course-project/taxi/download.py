import sys
from pathlib import Path

import requests

BASE = "https://d37ci6vzurychx.cloudfront.net"
DATA = Path(__file__).parent.parent / "data" / "nyc"


def download(url, path):
    if path.exists():
        print(f"skip {path.name}, already here")
        return
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        tmp = path.with_suffix(".part")
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                f.write(chunk)
        tmp.rename(path)
    print(f"downloaded {path.name}, {path.stat().st_size:,} bytes")


DATA.mkdir(parents=True, exist_ok=True)
for month in sys.argv[1:]:
    name = f"yellow_tripdata_{month}.parquet"
    download(f"{BASE}/trip-data/{name}", DATA / name)
download(f"{BASE}/misc/taxi_zone_lookup.csv", DATA / "taxi_zone_lookup.csv")