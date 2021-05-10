import React from "react";
import ReactDOM from "react-dom";

import { App } from "./app";
import "./i18n";
import "./scss/index.scss";

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById("root")
);
