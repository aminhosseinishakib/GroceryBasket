"""Export the validated annual price dataset as deterministic browser data."""

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILE = ROOT / "data" / "processed" / "annual_grocery_prices.csv"
OUTPUT_FILE = ROOT / "public" / "data" / "grocery-prices.json"
REQUIRED_COLUMNS = {
    "year", "series_id", "product", "definition", "category", "unit",
    "basket_quantity", "annual_average_price", "months_observed",
}


def read_rows() -> list[dict[str, str]]:
    with SOURCE_FILE.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames or not REQUIRED_COLUMNS.issubset(reader.fieldnames):
            raise ValueError("The processed dataset is missing required frontend-export columns.")
        return list(reader)


def build_export(rows: list[dict[str, str]]) -> dict[str, object]:
    products: dict[str, dict[str, object]] = {}
    prices: list[dict[str, object]] = []
    seen_prices: set[tuple[str, int]] = set()

    for row in rows:
        year = int(row["year"])
        series_id = row["series_id"]
        price = float(row["annual_average_price"])
        months_observed = int(row["months_observed"])
        quantity = float(row["basket_quantity"])
        key = (series_id, year)
        if price <= 0 or quantity < 0 or months_observed != 12:
            raise ValueError(f"Invalid processed value for {series_id} in {year}.")
        if key in seen_prices:
            raise ValueError(f"Duplicate processed price for {series_id} in {year}.")
        seen_prices.add(key)

        product = {
            "id": series_id,
            "name": row["product"],
            "definition": row["definition"],
            "category": row["category"],
            "unit": row["unit"],
            "defaultQuantity": quantity,
        }
        if series_id in products and products[series_id] != product:
            raise ValueError(f"Inconsistent metadata for {series_id}.")
        products[series_id] = product
        prices.append({"seriesId": series_id, "year": year, "price": price})

    return {
        "schemaVersion": 1,
        "products": sorted(products.values(), key=lambda item: (str(item["category"]), str(item["name"]))),
        "years": sorted({int(item["year"]) for item in prices}),
        "prices": sorted(prices, key=lambda item: (int(item["year"]), str(item["seriesId"]))),
    }


def main() -> None:
    export = build_export(read_rows())
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(export, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {len(export['products'])} products and {len(export['prices'])} prices to {OUTPUT_FILE}.")


if __name__ == "__main__":
    main()
