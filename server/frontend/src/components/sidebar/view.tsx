import { FunctionComponent } from "react";

import { Logo } from "../logo";
import { SidebarItem, SidebarItemProps } from "../sidebar-item";

export type SidebarViewProps = { items: SidebarItemProps[]; location: string };

export const SidebarView: FunctionComponent<SidebarViewProps> = (props) => {
  return (
    <div id="sidebar">
      <Logo key="sidebar-logo" className="sidebar-logo" />
      <ul key="sidebar-list" className="sidebar-menu">
        {props.items.map((item) => {
          if (item.path === props.location) {
            item.highlighted = true;
          } else {
            item.highlighted = false;
          }

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
