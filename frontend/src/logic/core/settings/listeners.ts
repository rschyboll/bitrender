import type { ListenersDef } from '@/logic/types';
import darkThemeText from '@/themes/dark.scss?inline';
import dimThemeText from '@/themes/dim.scss?inline';
import lightThemeText from '@/themes/light.scss?inline';
import { Theme } from '@/types/settings';

import type { SettingsLogicType } from './type';

export const Listeners: ListenersDef<SettingsLogicType> = {
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
};
