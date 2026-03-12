import React from "react";
import ReactDOM from "react-dom/client";
// Components
import App from "./App";
// Our CSS styles
import "./index.css";
// Bootstrap styles
import "bootstrap/dist/css/bootstrap.min.css";
// Bootstrap JS
import "bootstrap/dist/js/bootstrap.bundle.min.js";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
