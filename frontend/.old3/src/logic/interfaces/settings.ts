import { interfaces } from 'inversify';
import { Logic, LogicWrapper } from 'kea';

import { SidebarType, Theme } from '@/types/settings';

interface ISettings extends Logic {
  readonly actions: {
    readonly setTheme: (theme: Theme) => void;
    readonly setFontSize: (fontSize: number) => void;
    readonly setSidebarType: (type: SidebarType) => void;
    readonly toggleSidebar: (newState?: boolean) => void;
  };
  readonly values: {
    readonly theme: Theme;
    readonly fontSize: number;
    readonly sidebarType: SidebarType;
    readonly sidebarActive: boolean;
  };
}

export type ISettingsLogic = LogicWrapper<ISettings>;

export namespace ISettingsLogic {
  export const $: interfaces.ServiceIdentifier<ISettingsLogic> =
    Symbol('ISettingsLogic');
}
