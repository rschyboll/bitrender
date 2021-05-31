import { FunctionComponent } from "react";

import { Logo } from "../logo";
import { SidebarItem, SidebarItemProps } from "../sidebar-item";

export type SidebarViewProps = { items: SidebarItemProps[] };

export const SidebarView: FunctionComponent<SidebarViewProps> = (props) => {
  return (
    <div role="navigation" id="sidebar">
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
