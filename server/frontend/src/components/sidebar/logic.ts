import { SidebarItemProps } from "../sidebar-item";

export function highlightCurrentPath(items: SidebarItemProps[], path: string) {
  for (const item of items) {
    if (item.path === path) {
      item.highlighted = true;
    } else {
      item.highlighted = false;
    }
  }
  return [...items];
}
