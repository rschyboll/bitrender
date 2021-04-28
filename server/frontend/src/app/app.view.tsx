import React, { FunctionComponent } from "react";

import { Navbar } from "../components/navbar/navbar.container";

export const AppView: FunctionComponent = () => {
  return (
    <div id="content">
      <Navbar />
      <div></div>
    </div>
  );
};
