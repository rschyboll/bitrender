import { FunctionComponent } from "react";
import "./sidebar_item.scss";
import { SidebarItemProps } from "./sidebar_item.container";

import { Button } from "primereact/button";

export const SidebarItemView: FunctionComponent<SidebarItemProps> = (props) => {
  return (
    <div className="sidebar-item">
      <Button className="p-button-text p-button-plain" label={props.label} icon={props.icon} />
    </div>
  );
};
