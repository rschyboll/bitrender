import { FunctionComponent, useState } from "react";

import { SidebarView } from "./view";
import { SidebarItemProps } from "../sidebar-item";
import "./style.scss";

export const Sidebar: FunctionComponent = () => {
  const items = useState<SidebarItemProps[]>([
    { label: "Dashboard", icon: "pi pi-fw pi-home", path: "/" },
    { label: "Tasks", icon: "pi pi-fw pi-images", path: "/tasks" },
    { label: "Machines", icon: "pi pi-fw pi-desktop", path: "/machines" },
  ])[0];

  return <SidebarView items={items} />;
};
