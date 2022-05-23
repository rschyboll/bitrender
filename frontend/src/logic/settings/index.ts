import { actions, kea, path, reducers } from 'kea';

import type { settingsLogicType } from './indexType';
import { SidebarType, Theme } from './types';

export const settingsLogic = kea<settingsLogicType>([
  path(['settings']),
  actions({
    setSidebarType: (type: SidebarType) => ({ type }),
    setTheme: (theme: Theme) => ({ theme }),
    setSlimSidebarState: (sidebarState: boolean) => ({ sidebarState }),
    toggleMobileSidebar: true,
  }),
  reducers({
    theme: [
      Theme.Dark as Theme,
      { persist: true },
      {
        setTheme: (_, { theme }) => theme,
      },
    ],
    sidebarType: [
      SidebarType.Static as SidebarType,
      { persist: true },
      {
        setSidebarType: (_, { type }) => type,
      },
    ],
    sidebarSlimActive: [
      false,
      {
        setSlimSidebarState: (_, { sidebarState }) => sidebarState,
      },
    ],
    sidebarMobileActive: [
      false,
      {
        toggleMobileSidebar: (state) => !state,
      },
    ],
  }),
]);
