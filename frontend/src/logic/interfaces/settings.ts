import { Logic, LogicWrapper } from 'kea';

import { SidebarType, Theme } from '../core/settings/types';

interface ISettings extends Logic {
  readonly actions: {
    readonly setSidebarType: (type: SidebarType) => void;
    readonly setTheme: (theme: Theme) => void;
    readonly toggleSidebar: (newState?: boolean) => void;
  };
  readonly values: {
    readonly theme: Theme;
    readonly sidebarType: SidebarType;
    readonly sidebarActive: boolean;
  };
}

export type ISettingsLogic = LogicWrapper<ISettings>;
