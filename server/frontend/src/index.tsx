import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";

import { App } from "./app";
import { store } from "store";
import "./i18n";
import "./scss/index.scss";

ReactDOM.render(
  <React.StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>,
  document.getElementById("root")
);
