import { FunctionComponent } from "react";
import { SidebarItemView } from "./sidebar_item.view";

export type SidebarItemProps = {
  label: string;
  icon: string;
  path: string;
};

export const SidebarItem: FunctionComponent<SidebarItemProps> = (props) => {
  return <SidebarItemView {...props} />;
};
