<div align="center">

# 🛒 The Shrinking Grocery Basket

### See how far the same grocery budget goes across different years.

Compare the cost of a fixed basket of everyday groceries, explore which products changed the most, and simulate what still fits when prices rise but your budget stays the same.

[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react\&logoColor=white)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript\&logoColor=white)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-7-646CFF?logo=vite\&logoColor=white)](https://vite.dev/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python\&logoColor=white)](https://www.python.org/)
[![DuckDB](https://img.shields.io/badge/DuckDB-SQL-FFF000?logo=duckdb\&logoColor=black)](https://duckdb.org/)
[![GitHub Pages](https://img.shields.io/badge/Deployed%20with-GitHub%20Pages-222222?logo=github)](https://pages.github.com/)

### [View the Live Project](https://aminhosseinishakib.github.io/GroceryBasket/)

</div>

---

## About the Project

**The Shrinking Grocery Basket** is an interactive data storytelling project that explores a simple question:

> How has the purchasing power of a fixed grocery budget changed over time?

The application compares the cost of the same basket of groceries across two selected years. It shows what the full basket would have cost in the past, what it costs in the comparison year, and what may need to be reduced or removed to stay within a fixed budget.

The goal is to turn historical food-price data into something easy to understand, relatable, and interactive.

---

## What You Can Do

With the application, you can:

* Select a starting year
* Select a comparison year
* Set your grocery budget
* Review the full basket for both years
* Compare item-level and total price changes
* See how much money remains or how far the basket exceeds the budget
* Mark products as **Must Keep**, **Prefer to Keep**, or **Flexible**
* Simulate which quantities may be reduced or which products may be removed
* View dynamic key findings based on your selections
* Explore product-level and basket-level price trends
* Review the methodology, assumptions, and limitations

---

## How the Story Works

The app presents the analysis in three main stages:

### 1. What Your Budget Bought Before

The starting-year receipt shows the full grocery basket, including:

* Product quantities
* Unit prices
* Item costs
* Basket total
* Amount remaining or amount over budget

### 2. What the Same Basket Costs in the Comparison Year

The comparison-year receipt shows the cost of purchasing the exact same quantities in the selected comparison year.

This makes it easy to see:

* Total dollar change
* Percentage change
* Products with the largest increases
* How the selected budget performs across time

### 3. What Still Fits Within the Budget

When the comparison-year basket exceeds the selected budget, the app runs a transparent affordability simulation.

Users can protect the products that matter most by assigning priorities:

| Priority           | Meaning                                                     |
| ------------------ | ----------------------------------------------------------- |
| **Must Keep**      | The item is protected and will not be automatically changed |
| **Prefer to Keep** | The item is retained when possible                          |
| **Flexible**       | The item can be reduced or removed first                    |

The simulation clearly identifies products that are:

* Protected
* Unchanged
* Reduced
* Removed

> The affordability feature is a budget simulation, not nutritional or shopping advice.

---

## Basket Quantities

The project compares a fixed set of quantities across all years.

Each product includes:

* A clear basket quantity
* The source pricing unit
* A familiar quantity description
* An approximate real-world equivalent when appropriate

This helps visitors understand the difference between:

* The amount included in the basket
* The unit used by the source data
* The final cost displayed in each receipt

---

## Key Features

### Interactive Comparison Controls

Change the starting year, comparison year, and grocery budget to instantly update the full analysis.

### Receipt-Style Basket Views

Review the starting-year and comparison-year baskets using clear receipt-style layouts with aligned quantities and prices.

### Priority-Aware Budget Simulation

Protect important products and allow flexible ones to be adjusted first.

### Responsive Data Visualizations

Explore:

* Basket cost over time
* Product price changes
* Contribution to the total basket increase
* Category-level changes where supported

### Dynamic Key Findings

The application generates deterministic insights based on the current selection, including:

* Overall basket change
* Budget purchasing power
* Largest dollar increase
* Largest percentage increase
* Most stable item
* Largest contributor to basket growth
* Affordability simulation result

### Responsive Design

The interface is designed to work across:

* Desktop
* Laptop
* Tablet
* Mobile

---

## Technology Stack

### Data Analysis

* **Python** — data collection, processing, and validation
* **pandas** — cleaning and transformation
* **DuckDB** — analytical SQL queries
* **Pytest** — calculation and data-validation tests

### Frontend

* **React**
* **TypeScript**
* **Vite**
* **Tailwind CSS**
* **Recharts**

### Deployment

* **GitHub Pages**
* **GitHub Actions**

---

## Project Architecture

The project separates the data-analysis workflow from the public interface.

```text
Python data pipeline
        ↓
Processed grocery-price data
        ↓
Static JSON export
        ↓
React application
        ↓
Interactive analysis in the browser
```

The React application does not require a Python server while it is running.

The Python workflow prepares and validates the data, then exports frontend-safe JSON files that are loaded by the browser.

---

## Repository Structure

```text
GroceryBasket/
├── analysis/
│   ├── data/
│   │   ├── raw/
│   │   ├── interim/
│   │   └── processed/
│   ├── notebooks/
│   ├── scripts/
│   ├── sql/
│   ├── tests/
│   └── requirements.txt
│
├── scripts/
│   └── export_for_web.py
│
├── web/
│   ├── public/
│   │   └── data/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── types/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.ts
│   └── index.html
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── README.md
└── .gitignore
```

The exact folder structure may vary slightly as the project evolves.

---

## Running the Project Locally

### Prerequisites

Make sure you have:

* Python 3
* Node.js
* npm

---

### 1. Clone the Repository

```bash
git clone https://github.com/aminhosseinishakib/GroceryBasket.git
cd GroceryBasket
```

---

### 2. Create a Python Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

---

### 3. Install Python Dependencies

```powershell
pip install -r analysis\requirements.txt
```

Adjust the path if the Python requirements file is stored elsewhere.

---

### 4. Generate the Frontend Data

```powershell
python scripts\export_for_web.py
```

This creates or updates the JSON files used by the React application.

---

### 5. Install Frontend Dependencies

```powershell
cd web
npm install
```

---

### 6. Start the Development Server

```powershell
npm run dev
```

Open the local address shown in the terminal.

---

## Production Build

From the `web` directory:

```powershell
npm run build
```

Preview the production build locally:

```powershell
npm run preview
```

The generated site will be stored in:

```text
web/dist/
```

---

## Testing

### Frontend Tests

From the `web` directory:

```powershell
npm run test
```

### TypeScript and Build Validation

```powershell
npm run build
```

### Linting

```powershell
npm run lint
```

### Python Tests

From the project root:

```powershell
pytest
```

The test suite verifies calculations such as:

* Basket totals
* Dollar changes
* Percentage changes
* Budget remaining
* Amount over budget
* Product priority behavior
* Quantity reductions
* Removed-item order
* Protected-item shortfalls

---

## Data and Methodology

The project uses historical U.S. grocery price data prepared through a reproducible Python workflow.

The process includes:

1. Collecting and storing raw data
2. Validating source series and units
3. Cleaning product and date fields
4. Aggregating observations into yearly values
5. Applying unit conversions where required
6. Calculating fixed basket quantities
7. Running data-quality checks
8. Exporting a static dataset for the React application

The same product quantities are used across both selected years so that changes reflect differences in price rather than differences in basket composition.

---

## Main Calculations

For each product:

```text
Item cost = source price × basket quantity
```

For the full basket:

```text
Basket cost = sum of all item costs
```

The app also calculates:

* Dollar change between selected years
* Percentage change between selected years
* Amount remaining
* Amount over budget
* Product contribution to total basket growth
* Final simulated basket total

All calculations are deterministic and update based on the selected years, budget, and product priorities.

---

## Limitations

This project is intended to provide an understandable historical comparison, not an exact reconstruction of every household’s grocery spending.

Important limitations include:

* Prices are averages and may not represent every city, retailer, brand, or household.
* Product package sizes and quality may vary.
* Sales, coupons, taxes, loyalty discounts, and bulk pricing may not be included.
* The basket uses fixed quantities and does not adjust for household size.
* Approximate quantity equivalents are estimates rather than exact counts.
* The affordability simulation does not optimize nutrition or personal preference.
* Product substitutions and lower-cost brands are not automatically modeled.
* Historical product definitions and measurement units may change.
* Annual averages can hide price volatility within a year.
* The analysis does not identify the economic cause of individual price movements.
* The basket is illustrative and is not an official cost-of-living measure.

---

## Design Goals

The interface was designed to feel like a standalone data product rather than a traditional dashboard.

The design emphasizes:

* Clear storytelling
* Natural page flow
* Receipt-inspired comparisons
* Responsive layouts
* Accessible controls
* Consistent terminology
* Plain-language findings
* Transparent assumptions

---

## Future Improvements

Potential future additions include:

* Additional basket presets
* Regional price comparisons
* Household-size adjustments
* Product substitutions
* Nutrition-aware simulations
* Downloadable comparison summaries
* Additional historical economic indicators

These features are intentionally outside the current project scope so the application remains focused and easy to use.

---

## Author

**Amin Hosseini Shakib**

* [Portfolio](https://aminhosseinishakib.github.io/)
* [GitHub](https://github.com/aminhosseinishakib)
* [LinkedIn](https://www.linkedin.com/in/aminhosseinishakib/)

---

<div align="center">

### Explore how the same grocery budget changes across time.

[Open the Live App](https://aminhosseinishakib.github.io/GroceryBasket/)

</div>
