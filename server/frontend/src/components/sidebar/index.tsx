import { FunctionComponent, useState } from "react";
import { useLocation } from "react-router";

import { SidebarView } from "./view";
import { SidebarItemProps } from "../sidebar-item";
import "./style.scss";

export const Sidebar: FunctionComponent = () => {
  let location = useLocation().pathname;

  const items = useState<SidebarItemProps[]>([
    { label: "navigation.dashboard", icon: "pi pi-fw pi-home", path: "/" },
    { label: "navigation.tasks", icon: "pi pi-fw pi-images", path: "/tasks" },
    { label: "navigation.machines", icon: "pi pi-fw pi-desktop", path: "/machines" },
  ])[0];

  return <SidebarView items={items} location={location} />;
};
