import { actions, events, kea, listeners, path, reducers } from 'kea';

import { SidebarType, Theme, themeClasses } from '@/types/settings';

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
    setTheme: ({ theme }) => {
      const themeLink = document.getElementById('theme-link');
      if (themeLink instanceof HTMLLinkElement) {
        themeLink.href = `themes/${themeClasses[theme]}.css`;
      }
    },
    setFontSize: ({ fontSize }) => {
      console.log('TEST');
      const htmlElement = document.getElementsByTagName('html')[0];
      if (htmlElement instanceof HTMLHtmlElement) {
        console.log('TEST');
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
