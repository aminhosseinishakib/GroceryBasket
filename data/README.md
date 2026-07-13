# Data provenance

The source data are U.S. Bureau of Labor Statistics Average Price Data series. Raw inputs are downloaded as static CSV exports from FRED, which mirrors the BLS series IDs without requiring an API key:

- `data/raw/fred/*.csv` contains one unmodified monthly export for each selected BLS series.

The processed dataset retains the BLS series identifier, product definition, measurement unit, basket quantity, monthly-observation count, and annual average price. It includes eighteen common grocery products across pantry, protein, dairy, and produce. Annual values are arithmetic means of complete twelve-month calendar years. The first fully comparable default basket year is 1996 because the selected whole-milk series begins in July 1995. The application offers only years for which every user-selected product has all twelve monthly observations; it does not interpolate gaps.

Run from the repository root:

```powershell
python scripts/fetch_bls_average_prices.py
python scripts/build_annual_prices.py
python scripts/validate_dataset.py
python scripts/audit_monthly_coverage.py
```

The pipeline deliberately excludes any product-year without twelve monthly observations. It does not estimate missing prices or mix discontinued product definitions into the basket.
