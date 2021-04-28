import React from "react";
import ReactDOM from "react-dom";
import "./scss/index.scss";
import { App } from "./app/app.container";

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById("root")
);
