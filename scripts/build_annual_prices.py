"""Build an annual, comparable grocery-price dataset from BLS monthly data."""

import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw" / "fred"
OUTPUT_FILE = ROOT / "data" / "processed" / "annual_grocery_prices.csv"

PRODUCTS = {
    "APU0000701111": ("Flour", "Flour, white, all purpose", "Pantry", "lb", 5),
    "APU0000701312": ("Rice", "Rice, white, long grain, uncooked", "Pantry", "lb", 4),
    "APU0000701322": ("Spaghetti", "Spaghetti and macaroni", "Pantry", "lb", 2),
    "APU0000702111": ("Bread", "Bread, white, pan", "Pantry", "lb", 2),
    "APU0000702212": ("Whole wheat bread", "Bread, whole wheat, pan", "Pantry", "lb", 2),
    "APU0000703112": ("Ground beef", "Ground beef, 100% beef", "Protein", "lb", 2),
    "APU0000704111": ("Bacon", "Bacon, sliced", "Protein", "lb", 1),
    "APU0000706111": ("Whole chicken", "Chicken, fresh, whole", "Protein", "lb", 3),
    "APU0000FF1101": ("Boneless chicken breast", "Chicken breast, boneless", "Protein", "lb", 2),
    "APU0000708111": ("Eggs", "Eggs, Grade A, large", "Protein", "dozen", 1),
    "APU0000709112": ("Whole milk", "Milk, fresh, whole, fortified", "Dairy", "gallon", 1),
    "APU0000710212": ("Cheddar cheese", "Cheddar cheese, natural", "Dairy", "lb", 1),
    "APU0000711211": ("Bananas", "Bananas", "Produce", "lb", 2),
    "APU0000711311": ("Navel oranges", "Oranges, Navel", "Produce", "lb", 2),
    "APU0000712112": ("White potatoes", "Potatoes, white", "Produce", "lb", 3),
    "APU0000712211": ("Iceberg lettuce", "Lettuce, iceberg", "Produce", "lb", 1),
    "APU0000712311": ("Tomatoes", "Tomatoes, field grown", "Produce", "lb", 2),
    "APU0000714233": ("Dry beans", "Beans, dried, any type", "Pantry", "lb", 2),
}

DEFAULT_BASKET_SERIES_IDS = {
    "APU0000701312", "APU0000702111", "APU0000703112", "APU0000706111",
    "APU0000708111", "APU0000709112", "APU0000711211", "APU0000712112",
}


def parse_monthly_prices() -> dict[tuple[str, int], list[float]]:
    prices: dict[tuple[str, int], list[float]] = defaultdict(list)
    for series_id in PRODUCTS:
        source_file = RAW_DIR / f"{series_id}.csv"
        with source_file.open(newline="", encoding="utf-8") as source:
            for row in csv.DictReader(source):
                date = row["observation_date"]
                value = row[series_id]
                if value in {"", "."}:
                    continue
                prices[(series_id, int(date[:4]))].append(float(value))
    return prices


def main() -> None:
    if not RAW_DIR.exists():
        raise FileNotFoundError("Run scripts/fetch_bls_average_prices.py before building the dataset.")

    monthly_prices = parse_monthly_prices()
    rows = []
    for (series_id, year), values in sorted(monthly_prices.items()):
        if len(values) != 12:
            continue
        product, definition, category, unit, basket_quantity = PRODUCTS[series_id]
        rows.append(
            {
                "year": year,
                "series_id": series_id,
                "product": product,
                "definition": definition,
                "category": category,
                "unit": unit,
                "basket_quantity": basket_quantity,
                "annual_average_price": round(sum(values) / len(values), 4),
                "months_observed": len(values),
            }
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} annual product prices to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
