import { FunctionComponent } from "react";

import { SidebarItemView } from "./view";
import "./style.scss";

export type SidebarItemProps = {
  label: string;
  icon: string;
  path: string;
  highlighted?: boolean;
};

export const SidebarItem: FunctionComponent<SidebarItemProps> = (props) => {
  return <SidebarItemView {...props} />;
};
