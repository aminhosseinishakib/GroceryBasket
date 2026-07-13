import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { GroceryBasketApp } from "./components/GroceryBasketApp";
import "./styles.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <GroceryBasketApp />
  </StrictMode>,
);
