import { actions, kea, path, reducers } from 'kea';

import type { settingsLogicType } from './indexType';
import { SidebarType, Theme } from './types';

const logic = kea<settingsLogicType>([
  path(['settings']),
  actions({
    setSidebarType: (type: SidebarType) => ({ type }),
    setTheme: (theme: Theme) => ({ theme }),
    toggleSidebar: (newState?: boolean) => ({ newState }),
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
    sidebarActive: [
      false,
      {
        toggleSidebar: (state, { newState }) =>
          newState != null ? newState : !state,
      },
    ],
  }),
]);

export const settingsLogic = logic;
