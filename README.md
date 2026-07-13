# The Shrinking Grocery Basket

An interactive React app for comparing a selected grocery basket across time and testing how a fixed budget changes the basket.

## Features

- Compare the same basket between available years.
- Include or exclude 18 items, adjust quantities, and set priorities.
- Review item-level costs, totals, trends, and price-change contributors.
- Run a priority-aware budget simulation.
- Use light or dark mode.

## Data

The browser dataset is generated from processed annual grocery-price data. It uses U.S. city-average BLS Average Price series and a FRED series for boneless chicken breast. Prices are annual averages, not store-level prices.

The public browser dataset is [public/data/grocery-prices.json](public/data/grocery-prices.json). To regenerate it after changing the data pipeline:

```powershell
python scripts/export_frontend_data.py
```

## Run Locally

Requires Node.js 22.13 or newer.

```powershell
npm install
npm run dev
```

Open the local URL printed by Vite, normally `http://localhost:5173`.

## Validate

```powershell
python scripts/validate_dataset.py
npm test
```

## GitHub Pages

1. Create an empty GitHub repository and push this project to its `main` branch.
2. In the repository, open **Settings > Pages** and select **GitHub Actions** as the source.
3. Pushes to `main` automatically publish the app. Its address will be `https://<your-github-user>.github.io/<repository-name>/`.

The deployment workflow is in [.github/workflows/deploy-pages.yml](.github/workflows/deploy-pages.yml).

## Project Structure

- `src/`: interactive React application and calculations.
- `public/data/`: browser-ready grocery dataset.
- `data/`, `scripts/`, `sql/`, `notebooks/`: source data, validation, processing, and analysis workflow.
- `tests/`: static-build and dataset regression checks.
