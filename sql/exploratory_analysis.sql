-- Run after loading annual_grocery_prices.csv as a DuckDB table named prices.

-- Annual full-basket cost. Excludes every year without all eight products.
WITH default_prices AS (
    SELECT * FROM prices
    WHERE series_id IN ('APU0000701312', 'APU0000702111', 'APU0000703112', 'APU0000706111',
                        'APU0000708111', 'APU0000709112', 'APU0000711211', 'APU0000712112')
), complete_years AS (
    SELECT year
    FROM default_prices
    GROUP BY year
    HAVING COUNT(DISTINCT series_id) = 8
)
SELECT p.year,
       ROUND(SUM(p.annual_average_price * p.basket_quantity), 2) AS basket_cost
FROM default_prices p
JOIN complete_years y USING (year)
GROUP BY p.year
ORDER BY p.year;

-- Product-level price and basket-cost changes for the default comparison.
WITH default_prices AS (
    SELECT * FROM prices
    WHERE series_id IN ('APU0000701312', 'APU0000702111', 'APU0000703112', 'APU0000706111',
                        'APU0000708111', 'APU0000709112', 'APU0000711211', 'APU0000712112')
), base AS (
    SELECT * FROM default_prices WHERE year = 1996
), comparison AS (
    SELECT * FROM default_prices WHERE year = 2024
)
SELECT c.product,
       c.category,
       ROUND(b.annual_average_price, 2) AS price_1996,
       ROUND(c.annual_average_price, 2) AS price_2024,
       ROUND((c.annual_average_price / b.annual_average_price - 1) * 100, 1) AS percent_change,
       ROUND((c.annual_average_price - b.annual_average_price) * c.basket_quantity, 2) AS basket_cost_contribution
FROM base b
JOIN comparison c USING (series_id)
ORDER BY basket_cost_contribution DESC;

-- Coverage audit. Missing years are deliberately not imputed.
WITH default_prices AS (
    SELECT * FROM prices
    WHERE series_id IN ('APU0000701312', 'APU0000702111', 'APU0000703112', 'APU0000706111',
                        'APU0000708111', 'APU0000709112', 'APU0000711211', 'APU0000712112')
), all_years AS (
    SELECT * FROM generate_series(1996, 2025) AS t(year)
), observed AS (
    SELECT year, COUNT(DISTINCT series_id) AS product_count
    FROM default_prices
    GROUP BY year
)
SELECT a.year,
       COALESCE(o.product_count, 0) AS products_with_complete_observations,
       COALESCE(o.product_count, 0) = 8 AS usable_for_basket_comparison
FROM all_years a
LEFT JOIN observed o USING (year)
ORDER BY a.year;
