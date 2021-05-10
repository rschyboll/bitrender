import { FunctionComponent } from "react";
import { useLocation } from "react-router";

import { TopbarView } from "./view";
import "./style.scss";

export type TopbarProps = {};

export const Topbar: FunctionComponent<TopbarProps> = () => {
  let location = useLocation().pathname.replace("/", "");

  if (location === "") {
    location = "dashboard";
  }

  return <TopbarView location={location} />;
};
