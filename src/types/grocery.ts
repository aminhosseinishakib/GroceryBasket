export type GroceryProduct = {
  id: string;
  name: string;
  definition: string;
  category: string;
  unit: string;
  defaultQuantity: number;
};

export type ProductPriority = "must-keep" | "prefer-to-keep" | "flexible";

export type GroceryPrice = { seriesId: string; year: number; price: number };

export type GroceryDataset = {
  schemaVersion: number;
  products: GroceryProduct[];
  years: number[];
  prices: GroceryPrice[];
};
