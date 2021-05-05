import { FunctionComponent } from "react";
import { BrowserRouter, Switch, Route } from "react-router-dom";

import { Sidebar } from "../components/sidebar/sidebar.container";

export const AppView: FunctionComponent = () => {
  return (
    <div id="layout-base">
      <div id="layout-sidebar">
        <Sidebar />
        <BrowserRouter>
          <Switch>
            <Route path="/" />
          </Switch>
        </BrowserRouter>
      </div>
      <div id="layout-content"></div>
    </div>
  );
};
