import type { GroceryProduct, ProductPriority } from "../types/grocery";

export type BasketProductConfig = {
  priceBasis: string;
  reductionStep: number;
  minimumQuantity: number;
  canReduce: boolean;
  approximateEquivalent?: string;
};

export const priorityLabels: Record<ProductPriority, string> = {
  "must-keep": "Must keep",
  "prefer-to-keep": "Prefer to keep",
  flexible: "Flexible",
};

const poundConfig: BasketProductConfig = { priceBasis: "per lb", reductionStep: 1, minimumQuantity: 1, canReduce: true };

export const basketProductConfig: Record<string, BasketProductConfig> = {
  APU0000701111: { ...poundConfig, approximateEquivalent: "about 3 2/3 cups per lb" },
  APU0000701312: { ...poundConfig, approximateEquivalent: "about 2 1/4 cups uncooked per lb" },
  APU0000701322: { ...poundConfig, approximateEquivalent: "1 standard 16 oz box per lb" },
  APU0000702111: { ...poundConfig, approximateEquivalent: "about 1/2 large sliced loaf per lb" },
  APU0000702212: { ...poundConfig, approximateEquivalent: "about 1/2 large sliced loaf per lb" },
  APU0000703112: { ...poundConfig, approximateEquivalent: "1 one-pound pack per lb" },
  APU0000704111: { ...poundConfig, approximateEquivalent: "1 standard 16 oz package per lb" },
  APU0000706111: { ...poundConfig, approximateEquivalent: "about 1/3 small whole chicken per lb" },
  APU0000FF1101: { ...poundConfig, approximateEquivalent: "about 1 to 1 1/2 servings per lb" },
  APU0000708111: { priceBasis: "per dozen", reductionStep: 1, minimumQuantity: 1, canReduce: false, approximateEquivalent: "12 large eggs per dozen" },
  APU0000709112: { priceBasis: "per gallon", reductionStep: 1, minimumQuantity: 1, canReduce: false, approximateEquivalent: "16 cups per gallon" },
  APU0000710212: { ...poundConfig, approximateEquivalent: "about 4 cups shredded per lb" },
  APU0000711211: { ...poundConfig, approximateEquivalent: "about 3 to 4 medium bananas per lb" },
  APU0000711311: { ...poundConfig, approximateEquivalent: "about 2 medium oranges per lb" },
  APU0000712112: { ...poundConfig, approximateEquivalent: "about 2 medium potatoes per lb" },
  APU0000712211: { ...poundConfig, approximateEquivalent: "1 large iceberg head per lb" },
  APU0000712311: { ...poundConfig, approximateEquivalent: "about 2 to 3 medium tomatoes per lb" },
  APU0000714233: { ...poundConfig, approximateEquivalent: "about 2 1/4 cups dry beans per lb" },
};

export function getBasketProductConfig(product: GroceryProduct): BasketProductConfig {
  return basketProductConfig[product.id] ?? { priceBasis: `per ${product.unit}`, reductionStep: 1, minimumQuantity: 1, canReduce: false };
}

export function quantityLabel(quantity: number, unit: string): string {
  if (unit === "lb") return `${quantity} lb`;
  if (unit === "gallon") return `${quantity} ${quantity === 1 ? "gallon" : "gallons"}`;
  if (unit === "dozen") return `${quantity} dozen`;
  return `${quantity} ${unit}`;
}
