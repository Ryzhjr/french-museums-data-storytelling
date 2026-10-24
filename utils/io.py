"""Read the two local data files."""

import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def load_data():
    return pd.read_csv(ROOT / "data" / "ENTREES_ET_CATEGORIES_DE_PUBLIC.csv",
                       sep=";", encoding="utf-8", dtype="string")


def load_geojson():
    with open(ROOT / "data" / "regions.geojson", encoding="utf-8") as file:
        return json.load(file)
