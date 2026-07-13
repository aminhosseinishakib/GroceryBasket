"""Run the project’s exploratory DuckDB analysis and save reusable result tables."""

from pathlib import Path

import duckdb

from build_annual_prices import DEFAULT_BASKET_SERIES_IDS


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data" / "processed" / "annual_grocery_prices.csv"
OUTPUT_DIR = ROOT / "data" / "analysis"
BASE_YEAR = 1996
COMPARISON_YEAR = 2024


def export(con: duckdb.DuckDBPyConnection, query: str, filename: str) -> None:
    destination = OUTPUT_DIR / filename
    con.execute(f"COPY ({query}) TO '{destination.as_posix()}' (HEADER, DELIMITER ',')")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    con.execute(
        "CREATE TABLE prices AS SELECT * FROM read_csv_auto(?, header = true)",
        [str(DATASET)],
    )
    default_series_sql = ", ".join(f"'{series_id}'" for series_id in sorted(DEFAULT_BASKET_SERIES_IDS))
    con.execute(f"CREATE TABLE default_prices AS SELECT * FROM prices WHERE series_id IN ({default_series_sql})")
    con.execute(
        """
        CREATE TABLE complete_years AS
        SELECT year
        FROM default_prices
        GROUP BY year
        HAVING COUNT(DISTINCT series_id) = 8
        """
    )

    basket_costs = """
        SELECT p.year,
               ROUND(SUM(p.annual_average_price * p.basket_quantity), 2) AS basket_cost
        FROM default_prices p
        JOIN complete_years y USING (year)
        GROUP BY p.year
        ORDER BY p.year
    """
    item_changes = f"""
        WITH base AS (
            SELECT * FROM default_prices WHERE year = {BASE_YEAR}
        ), comparison AS (
            SELECT * FROM default_prices WHERE year = {COMPARISON_YEAR}
        )
        SELECT c.product,
               c.category,
               c.unit,
               c.basket_quantity,
               ROUND(b.annual_average_price, 2) AS base_price,
               ROUND(c.annual_average_price, 2) AS comparison_price,
               ROUND(c.annual_average_price - b.annual_average_price, 2) AS unit_change,
               ROUND((c.annual_average_price / b.annual_average_price - 1) * 100, 1) AS percent_change,
               ROUND((c.annual_average_price - b.annual_average_price) * c.basket_quantity, 2) AS basket_cost_contribution
        FROM base b
        JOIN comparison c USING (series_id)
        ORDER BY basket_cost_contribution DESC
    """
    category_contribution = f"""
        WITH item_changes AS ({item_changes})
        SELECT category,
               ROUND(SUM(basket_cost_contribution), 2) AS dollar_contribution,
               ROUND(SUM(basket_cost_contribution) / SUM(SUM(basket_cost_contribution)) OVER () * 100, 1) AS share_of_basket_increase
        FROM item_changes
        GROUP BY category
        ORDER BY dollar_contribution DESC
    """
    availability = """
        WITH all_years AS (
            SELECT * FROM generate_series(1996, 2025) AS t(year)
        ), observed AS (
            SELECT year, COUNT(DISTINCT series_id) AS products_with_complete_observations
            FROM default_prices
            GROUP BY year
        )
        SELECT a.year,
               COALESCE(o.products_with_complete_observations, 0) AS products_with_complete_observations,
               CASE WHEN COALESCE(o.products_with_complete_observations, 0) = 8
                    THEN 'supported'
                    ELSE 'excluded: incomplete basket coverage'
               END AS status
        FROM all_years a
        LEFT JOIN observed o USING (year)
        ORDER BY a.year
    """

    export(con, basket_costs, "basket_costs.csv")
    export(con, item_changes, "item_changes_1996_to_2024.csv")
    export(con, category_contribution, "category_contribution_1996_to_2024.csv")
    export(con, availability, "year_availability.csv")

    start_cost, end_cost = con.execute(
        f"SELECT MIN(CASE WHEN year = {BASE_YEAR} THEN basket_cost END), MIN(CASE WHEN year = {COMPARISON_YEAR} THEN basket_cost END) FROM ({basket_costs})"
    ).fetchone()
    top_item = con.execute(item_changes).fetchone()
    print(f"Basket cost: ${start_cost:.2f} in {BASE_YEAR}; ${end_cost:.2f} in {COMPARISON_YEAR}.")
    print(f"Change: {(end_cost / start_cost - 1) * 100:.1f}%.")
    print(f"Largest basket-cost contributor: {top_item[0]} (${top_item[-1]:.2f}).")
    print(f"Saved analysis tables to {OUTPUT_DIR}.")


if __name__ == "__main__":
    main()
