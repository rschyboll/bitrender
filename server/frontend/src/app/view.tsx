import { FunctionComponent } from "react";
import { BrowserRouter } from "react-router-dom";

import { Sidebar } from "../components/sidebar";

export const AppView: FunctionComponent = () => {
  return (
    <div id="layout-base">
      <div id="layout-sidebar">
        <BrowserRouter>
          <Sidebar />
        </BrowserRouter>
      </div>
      <div id="layout-content"></div>
    </div>
  );
};
