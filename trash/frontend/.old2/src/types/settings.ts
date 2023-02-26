export enum SidebarType {
  Static,
  Slim,
  Horizontal,
}

export enum Theme {
  Dark,
  Dim,
  Light,
}
export const layoutTypesClasses = {
  [SidebarType.Horizontal]: 'layout-horizontal',
  [SidebarType.Slim]: 'layout-slim',
  [SidebarType.Static]: 'layout-static',
};

export const themeClasses = {
  [Theme.Dark]: 'dark',
  [Theme.Dim]: 'dim',
  [Theme.Light]: 'light',
};
