import { getBasketProductConfig } from "./basket-config";
import type { GroceryDataset, GroceryProduct, ProductPriority } from "../types/grocery";

export type BasketItem = GroceryProduct & { included: boolean; quantity: number; priority: ProductPriority };
export type Adjustment = "unchanged" | "reduced" | "removed";
export type ComparisonRow = BasketItem & {
  basePrice: number;
  currentPrice: number;
  baseCost: number;
  currentCost: number;
  contribution: number;
  percentChange: number;
  adjustedQuantity: number;
  adjustment: Adjustment;
  removed: boolean;
};

const priceKey = (seriesId: string, year: number) => `${seriesId}:${year}`;
const priorityOrder: ProductPriority[] = ["flexible", "prefer-to-keep"];

export function availableYears(dataset: GroceryDataset, basket: BasketItem[]): number[] {
  const active = basket.filter((item) => item.included && item.quantity > 0);
  if (!active.length) return [];
  const prices = new Set(dataset.prices.map((price) => priceKey(price.seriesId, price.year)));
  return dataset.years.filter((year) => active.every((item) => prices.has(priceKey(item.id, year))));
}

function adjustedTotal(rows: ComparisonRow[]) {
  return rows.reduce((total, row) => total + row.currentPrice * row.adjustedQuantity, 0);
}

function reducePriority(rows: ComparisonRow[], priority: ProductPriority, budget: number) {
  while (adjustedTotal(rows) > budget) {
    const candidates = rows.filter((row) => {
      const config = getBasketProductConfig(row);
      return row.priority === priority && config.canReduce && row.adjustedQuantity - config.reductionStep >= config.minimumQuantity;
    }).sort((left, right) => {
      const leftConfig = getBasketProductConfig(left);
      const rightConfig = getBasketProductConfig(right);
      return right.currentPrice * rightConfig.reductionStep - left.currentPrice * leftConfig.reductionStep;
    });
    const candidate = candidates[0];
    if (!candidate) return;
    const config = getBasketProductConfig(candidate);
    candidate.adjustedQuantity -= config.reductionStep;
    candidate.adjustment = "reduced";
  }
}

function removePriority(rows: ComparisonRow[], priority: ProductPriority, budget: number) {
  const candidates = rows.filter((row) => row.priority === priority && row.adjustedQuantity > 0)
    .sort((left, right) => right.currentPrice * right.adjustedQuantity - left.currentPrice * left.adjustedQuantity);
  for (const candidate of candidates) {
    if (adjustedTotal(rows) <= budget) return;
    candidate.adjustedQuantity = 0;
    candidate.adjustment = "removed";
    candidate.removed = true;
  }
}

export function compareBasket(
  dataset: GroceryDataset,
  basket: BasketItem[],
  baseYear: number,
  comparisonYear: number,
  budget: number,
) {
  const lookup = new Map(dataset.prices.map((price) => [priceKey(price.seriesId, price.year), price.price]));
  const rows: ComparisonRow[] = [];
  for (const item of basket.filter((entry) => entry.included && entry.quantity > 0)) {
    const basePrice = lookup.get(priceKey(item.id, baseYear));
    const currentPrice = lookup.get(priceKey(item.id, comparisonYear));
    if (basePrice === undefined || currentPrice === undefined) continue;
    const baseCost = basePrice * item.quantity;
    const currentCost = currentPrice * item.quantity;
    rows.push({ ...item, basePrice, currentPrice, baseCost, currentCost, contribution: currentCost - baseCost, percentChange: (currentPrice / basePrice - 1) * 100, adjustedQuantity: item.quantity, adjustment: "unchanged", removed: false });
  }
  rows.sort((left, right) => right.contribution - left.contribution);

  const baseTotal = rows.reduce((total, row) => total + row.baseCost, 0);
  const currentTotal = rows.reduce((total, row) => total + row.currentCost, 0);
  for (const priority of priorityOrder) {
    reducePriority(rows, priority, budget);
    removePriority(rows, priority, budget);
  }
  const remainingTotal = adjustedTotal(rows);
  const protectedShortfall = Math.max(0, remainingTotal - budget);

  return {
    rows,
    baseTotal,
    currentTotal,
    remainingTotal,
    budgetDifference: budget - currentTotal,
    adjustedBudgetDifference: budget - remainingTotal,
    protectedShortfall,
  };
}

export function basketCostByYear(dataset: GroceryDataset, basket: BasketItem[], years: number[]) {
  const lookup = new Map(dataset.prices.map((price) => [priceKey(price.seriesId, price.year), price.price]));
  const active = basket.filter((item) => item.included && item.quantity > 0);
  return years.map((year) => ({ year, cost: active.reduce((total, item) => total + (lookup.get(priceKey(item.id, year)) ?? 0) * item.quantity, 0) }));
}
