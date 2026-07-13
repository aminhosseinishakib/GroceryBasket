"""Validate coverage and numeric integrity of the processed annual dataset."""

import csv
from collections import defaultdict
from pathlib import Path

from build_annual_prices import DEFAULT_BASKET_SERIES_IDS


DATASET = Path(__file__).resolve().parents[1] / "data" / "processed" / "annual_grocery_prices.csv"
MINIMUM_COMPLETE_YEARS = 20


def main() -> None:
    if not DATASET.exists():
        raise FileNotFoundError("Build the processed dataset before validating it.")

    coverage: dict[int, set[str]] = defaultdict(set)
    with DATASET.open(newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            year = int(row["year"])
            price = float(row["annual_average_price"])
            months = int(row["months_observed"])
            if price <= 0:
                raise ValueError(f"Non-positive annual price for {row['series_id']} in {year}.")
            if months != 12:
                raise ValueError(f"Incomplete annual observation for {row['series_id']} in {year}.")
            coverage[year].add(row["series_id"])

    complete_years = sorted(year for year, series_ids in coverage.items() if DEFAULT_BASKET_SERIES_IDS.issubset(series_ids))
    if len(complete_years) < MINIMUM_COMPLETE_YEARS:
        raise ValueError(f"Only {len(complete_years)} complete annual baskets were found.")
    print(f"Validation passed: {len(complete_years)} complete annual baskets.")
    print(f"Supported years: {', '.join(map(str, complete_years))}")


if __name__ == "__main__":
    main()
