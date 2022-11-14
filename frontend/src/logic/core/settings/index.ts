import { actions, events, kea, listeners, path, reducers } from 'kea';

import { SidebarType, Theme } from '@/types/settings';

import { Listeners } from './listeners';
import { Reducers } from './reducers';
import type { SettingsLogicType } from './type';

const logic = kea<SettingsLogicType>([
  path(['settings']),
  actions({
    setFontSize: (fontSize: number) => ({ fontSize }),
    setSidebarType: (type: SidebarType) => ({ type }),
    setTheme: (theme: Theme) => ({ theme }),
    toggleSidebar: (newState?: boolean) => ({ newState }),
  }),
  reducers(Reducers),
  listeners(Listeners),
  events(({ actions, values }) => ({
    afterMount: [
      () => actions.setFontSize(values.fontSize),
      () => actions.setTheme(values.theme),
    ],
  })),
]);

export const settingsLogic = logic;
