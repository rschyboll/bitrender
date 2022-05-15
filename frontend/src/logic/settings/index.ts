import { actions, kea, reducers } from 'kea';

import type { settingsLogicType } from './indexType';
import { SidebarType, Theme } from './types';

export const settingsLogic = kea<settingsLogicType>([
  actions({
    setSidebarType: (type: SidebarType) => ({ type }),
    setTheme: (theme: Theme) => ({ theme }),
    toggleOverlaySidebar: true,
    toggleMobileSidebar: true,
  }),
  reducers({
    theme: [
      Theme.Dark as Theme,
      {
        setTheme: (_, { theme }) => theme,
      },
    ],
    sidebarType: [
      SidebarType.Static as SidebarType,
      {
        setSidebarType: (_, { type }) => type,
      },
    ],
    sidebarOverlayActive: [
      false,
      {
        toggleOverlaySidebar: (state) => !state,
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
