import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import ColorWheel from "./ColorWheel";

const appRoot = document.getElementById("root");
if (appRoot) {
  createRoot(appRoot).render(
    <StrictMode>
      <App />
    </StrictMode>
  );
}

const colorWheelTarget = document.getElementById("color-wheel-root");
if (colorWheelTarget) {
  createRoot(colorWheelTarget).render(
    <StrictMode>
      <ColorWheel
        initialDate={colorWheelTarget.getAttribute("data-date") ?? undefined}
      />
    </StrictMode>
  );
}