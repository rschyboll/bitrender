import { FunctionComponent } from "react";
import { Sidebar } from "../components/sidebar/sidebar.container";

export const AppView: FunctionComponent = () => {
  return (
    <div id="layout-base">
      <div id="layout-sidebar">
        <Sidebar />
      </div>
      <div id="layout-content"></div>
    </div>
  );
};
