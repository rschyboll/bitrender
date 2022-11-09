import { actions, events, kea, listeners, path, reducers } from 'kea';

import darkThemeText from '@/themes/dark.scss?inline';
import dimThemeText from '@/themes/dim.scss?inline';
import lightThemeText from '@/themes/light.scss?inline';
import { SidebarType, Theme } from '@/types/settings';

import type { logicType } from './indexType';

const logic = kea<logicType>([
  path(['settings']),
  actions({
    setFontSize: (fontSize: number) => ({ fontSize }),
    setSidebarType: (type: SidebarType) => ({ type }),
    setTheme: (theme: Theme) => ({ theme }),
    toggleSidebar: (newState?: boolean) => ({ newState }),
  }),
  reducers({
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
  }),
  listeners({
    setTheme: async ({ theme }) => {
      const themeLink = document.getElementById('theme-link');
      if (themeLink instanceof HTMLStyleElement) {
        if (theme == Theme.Dark) {
          themeLink.textContent = darkThemeText;
        } else if (theme == Theme.Light) {
          themeLink.textContent = lightThemeText;
        } else if (theme == Theme.Dim) {
          themeLink.textContent = dimThemeText;
        }
      }
    },
    setFontSize: async ({ fontSize }, breakpoint) => {
      await breakpoint(200);
      const htmlElement = document.getElementsByTagName('html')[0];
      if (htmlElement instanceof HTMLHtmlElement) {
        htmlElement.style.fontSize = fontSize.toString() + 'px';
      }
    },
  }),
  events(({ actions, values }) => ({
    afterMount: [
      () => actions.setFontSize(values.fontSize),
      () => actions.setTheme(values.theme),
    ],
  })),
]);

export const settingsLogic = logic;
