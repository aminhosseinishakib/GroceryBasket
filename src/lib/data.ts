import type { GroceryDataset } from "../types/grocery";

export async function loadGroceryDataset(): Promise<GroceryDataset> {
  const response = await fetch(`${import.meta.env.BASE_URL}data/grocery-prices.json`);
  if (!response.ok) throw new Error("The grocery price data could not be loaded.");

  const dataset = (await response.json()) as GroceryDataset;
  if (dataset.schemaVersion !== 1 || !dataset.products.length || !dataset.prices.length) {
    throw new Error("The grocery price data is incomplete.");
  }
  return dataset;
}
