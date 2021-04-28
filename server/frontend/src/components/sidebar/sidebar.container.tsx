import { FunctionComponent, useState } from "react";

import { SidebarView } from "./sidebar.view";
import { SidebarItemProps } from "../sidebar_item/sidebar_item.container";

export const Sidebar: FunctionComponent = () => {
  const testCommand = (event: any) => {};

  const items = useState<SidebarItemProps[]>([
    { label: "Dashboard", icon: "pi pi-fw pi-home", command: testCommand },
    { label: "Tasks", icon: "pi pi-fw pi-images", command: testCommand },
    { label: "Machines", icon: "pi pi-fw pi-desktop", command: testCommand },
  ])[0];

  return <SidebarView items={items} />;
};
