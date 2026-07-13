"""Document each missing monthly observation in the selected source series."""

import csv
from collections import defaultdict
from pathlib import Path

from build_annual_prices import PRODUCTS


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw" / "fred"
OUTPUT_FILE = ROOT / "data" / "analysis" / "missing_observations.csv"
YEARS = range(1996, 2026)


def main() -> None:
    output_rows = []
    for series_id, (product, _, _, _, _) in PRODUCTS.items():
        observed: dict[int, set[int]] = defaultdict(set)
        with (RAW_DIR / f"{series_id}.csv").open(newline="", encoding="utf-8") as source:
            for row in csv.DictReader(source):
                if row[series_id] in {"", "."}:
                    continue
                year, month, _ = row["observation_date"].split("-")
                observed[int(year)].add(int(month))
        for year in YEARS:
            missing_months = [month for month in range(1, 13) if month not in observed[year]]
            if missing_months:
                output_rows.append(
                    {
                        "year": year,
                        "series_id": series_id,
                        "product": product,
                        "months_observed": 12 - len(missing_months),
                        "missing_months": ", ".join(f"{month:02d}" for month in missing_months),
                    }
                )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=output_rows[0].keys())
        writer.writeheader()
        writer.writerows(output_rows)
    print(f"Recorded {len(output_rows)} product-year coverage gaps in {OUTPUT_FILE}.")


if __name__ == "__main__":
    main()
