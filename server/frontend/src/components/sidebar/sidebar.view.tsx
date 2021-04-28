import { FunctionComponent } from "react";
import "./sidebar.scss";

import { Logo } from "../logo/logo";
import { SidebarItem, SidebarItemProps } from "../sidebar_item/sidebar_item.container";

export const SidebarView: FunctionComponent<{ items: SidebarItemProps[] }> = (props) => {
  return (
    <div id="sidebar">
      <Logo key="sidebar-logo" className="sidebar-logo" />
      <ul key="sidebar-list" className="sidebar-menu">
        {props.items.map((item) => {
          return (
            <li key={item.label}>
              <div className="sidebar-separator" />
              <SidebarItem {...item} />
            </li>
          );
        })}
      </ul>
    </div>
  );
};
