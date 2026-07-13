-- Annual basket completeness: every supported year must contain all eight products.
SELECT year, COUNT(DISTINCT series_id) AS product_count
FROM annual_grocery_prices
GROUP BY year
HAVING COUNT(DISTINCT series_id) <> 8;

-- Only full-year averages belong in the portfolio analysis.
SELECT year, product, months_observed
FROM annual_grocery_prices
WHERE months_observed <> 12;

-- Prices must remain positive after the transformation.
SELECT year, product, annual_average_price
FROM annual_grocery_prices
WHERE annual_average_price <= 0;
