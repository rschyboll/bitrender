import { FunctionComponent, MouseEvent } from "react";
import { SidebarItemView } from "./sidebar_item.view";

export type SidebarItemProps = {
  label: string;
  icon: string;
  command: (event: MouseEvent) => void;
};

export const SidebarItem: FunctionComponent<SidebarItemProps> = (props) => {
  return <SidebarItemView {...props} />;
};
