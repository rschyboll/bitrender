/* eslint-disable @typescript-eslint/no-dynamic-delete */
import type { ReducersDef } from '@/logic';
import { SidebarType, Theme } from '@/types/settings';

import type { SettingsLogicType } from './type';

export const Reducers: ReducersDef<SettingsLogicType> = {
  fontSize: [
    14,
    {
      persist: true,
    },
    {
      setFontSize: (_, { fontSize }) => fontSize,
    },
  ],
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
};
