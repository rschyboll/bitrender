import { FunctionComponent } from "react";
import { useLocation } from "react-router";

import { TopbarView } from "./view";
import "./style.scss";

export const Topbar: FunctionComponent<{}> = () => {
  let location = useLocation().pathname.replace("/", "");

  if (location === "") {
    location = "dashboard";
  }

  return <TopbarView location={location} />;
};
