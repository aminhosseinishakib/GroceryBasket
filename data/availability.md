# Why some years are unavailable

The app will include a year only when all eight selected BLS price series have twelve monthly observations for that calendar year. This rule protects the comparison from two avoidable distortions:

1. A partial-year average can reflect seasonality rather than a true annual price level.
2. Replacing an unavailable item with a different product definition would break comparability across years.

The current extract therefore excludes 2000–2002, 2012, 2020, and 2025. The coverage audit names the exact missing series and months in `data/analysis/missing_observations.csv`.

- 2000: rice is missing May through December; 2001 has no rice observations; and 2002 rice is missing January through April.
- 2012: ground beef is missing October.
- 2020: rice is missing April, whole chicken is missing May, and white potatoes are missing March and April.
- 2025: rice, bread, ground beef, whole chicken, eggs, whole milk, and bananas are missing October; white potatoes are missing October and November. These are source-publication gaps, not values of zero.

The project does not interpolate, carry a price forward, or substitute another series.
