import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const projectRoot = new URL("../", import.meta.url);

test("builds a static GitHub Pages entry point", async () => {
  const html = await readFile(new URL("dist/index.html", projectRoot), "utf8");

  assert.match(html, /The Shrinking Grocery Basket/);
  assert.match(html, /id="root"/);
  assert.match(html, /type="module"/);
  assert.doesNotMatch(html, /Your site is taking shape|Codex is working/);
});

test("ships a complete deterministic browser dataset", async () => {
  const source = await readFile(new URL("public/data/grocery-prices.json", projectRoot), "utf8");
  const data = JSON.parse(source);

  assert.equal(data.schemaVersion, 1);
  assert.equal(data.products.length, 18);
  assert.equal(data.prices.length, 675);
  assert.ok(data.years.includes(1996));
  assert.ok(data.years.includes(2024));
  assert.ok(data.products.every((product) => product.id && product.name && product.unit));
  assert.ok(data.prices.every((price) => price.price > 0 && Number.isInteger(price.year)));
  assert.ok(data.products.some((product) => product.name === "Boneless chicken breast"));
  assert.ok(!data.products.some((product) => product.name === "Chicken legs"));
});

test("keeps the public-facing basket and data-source copy", async () => {
  const source = await readFile(new URL("src/components/GroceryBasketApp.tsx", projectRoot), "utf8");

  assert.match(source, /Available comparison range/);
  assert.match(source, /Starting-year basket/);
  assert.match(source, /Comparison-year basket/);
  assert.match(source, /Budget-fit basket/);
  assert.match(source, /Priority-aware simulation/);
  assert.match(source, /BLS Average Price Data/);
  assert.match(source, /FRED data sources/);
  assert.doesNotMatch(source, /FRED series APU0000FF1101/);
});
