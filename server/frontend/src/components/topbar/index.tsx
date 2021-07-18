import { FunctionComponent } from "react";
import { useLocation } from "react-router";

import { TopbarView } from "./view";
import { getPathName } from "./logic";
import "./style.scss";

export type TopbarProps = {};

export const Topbar: FunctionComponent<TopbarProps> = () => {
  const location = useLocation();
  const pathName = getPathName(location);

  return <TopbarView pathName={pathName} />;
};
