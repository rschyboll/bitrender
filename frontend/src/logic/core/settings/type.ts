import type { MakeOwnLogicType } from '@/logic/types';
import { SidebarType, Theme } from '@/types/settings';

interface Actions {
  setFontSize: (fontSize: number) => { fontSize: number };
  setSidebarType: (type: SidebarType) => { type: SidebarType };
  setTheme: (theme: Theme) => { theme: Theme };
  toggleSidebar: (newState?: boolean) => { newState?: boolean };
}

interface Reducers {
  fontSize: number;
  theme: Theme;
  sidebarType: SidebarType;
  sidebarActive: boolean;
}

export type SettingsLogicType = MakeOwnLogicType<{
  actions: Actions;
  reducers: Reducers;
}>;
