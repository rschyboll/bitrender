import { FunctionComponent, useState, useEffect } from "react";
import { useLocation } from "react-router";

import { SidebarView } from "./view";
import { highlightCurrentPath } from "./logic";
import { SidebarItemProps } from "../sidebar-item";
import "./style.scss";

const sidebarItems = [
  { label: "navigation.dashboard", icon: "pi pi-fw pi-home", path: "/" },
  { label: "navigation.tasks", icon: "pi pi-fw pi-images", path: "/tasks" },
  {
    label: "navigation.machines",
    icon: "pi pi-fw pi-desktop",
    path: "/workers",
  },
  {
    label: "navigation.binaries",
    icon: "pi pi-fw pi-microsoft",
    path: "/binaries",
  },
];

export const Sidebar: FunctionComponent = () => {
  let location = useLocation().pathname;
  const [items, setItems] = useState<SidebarItemProps[]>(sidebarItems);

  useEffect(() => {
    setItems((items) => highlightCurrentPath(items, location));
  }, [location]);

  return <SidebarView items={items} />;
};
