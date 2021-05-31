import { FunctionComponent, useState, useEffect } from "react";
import { useLocation } from "react-router";

import { SidebarView } from "./view";
import { SidebarItemProps } from "../sidebar-item";
import "./style.scss";
import { highlightCurrentPath } from "./logic";

const sidebarItems = [
  { label: "navigation.dashboard", icon: "pi pi-fw pi-home", path: "/" },
  { label: "navigation.tasks", icon: "pi pi-fw pi-images", path: "/tasks" },
  { label: "navigation.machines", icon: "pi pi-fw pi-desktop", path: "/machines" },
];

export const Sidebar: FunctionComponent = () => {
  let location = useLocation().pathname;
  const [items, setItems] = useState<SidebarItemProps[]>(sidebarItems);

  useEffect(() => {
    setItems((items) => highlightCurrentPath(items, location));
  }, [location]);

  return <SidebarView items={items} />;
};
