import { FunctionComponent } from "react";
import "./sidebar_item.scss";
import { Link } from "react-router-dom";
import { Button } from "primereact/button";

import { SidebarItemProps } from ".";

export const SidebarItemView: FunctionComponent<SidebarItemProps> = (props) => {
  return (
    <Link id="test" className="sidebar-item" to={props.path}>
      <Button className="p-button-text p-button-plain" label={props.label} icon={props.icon} />
    </Link>
  );
};
