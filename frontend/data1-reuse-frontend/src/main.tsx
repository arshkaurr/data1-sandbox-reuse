import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import ColorWheel from "./ColorWheel";
import VisitorsDashboard from "./VisitorsDashboard";

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

const visitorsRoot = document.getElementById("visitors-root");
if (visitorsRoot) {
  const dataset = visitorsRoot.dataset;
  createRoot(visitorsRoot).render(
    <StrictMode>
      <VisitorsDashboard
        endpoint={dataset.endpoint ?? ""}
        submitUrl={dataset.submitUrl ?? "/visitors/submit/"}
        csrfToken={dataset.csrf ?? ""}
        location={dataset.location ?? ""}
        userEmail={dataset.userEmail ?? undefined}
        homeUrl={dataset.homeUrl ?? undefined}
      />
    </StrictMode>
  );
}
