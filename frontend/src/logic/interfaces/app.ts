import { interfaces } from 'inversify';
import { Logic, LogicWrapper } from 'kea';

interface IApp extends Logic {
  readonly actions: {
    readonly openApp: () => void;
    readonly openLoginPage: () => void;
    readonly openRegisterPage: () => void;
    readonly openUsersPage: () => void;
    readonly openRolesPage: () => void;
    readonly openErrorPage: () => void;
  };
  readonly values: {};
}

export type IAppLogic = LogicWrapper<IApp>;

export namespace IAppLogic {
  export const $: interfaces.ServiceIdentifier<IAppLogic> = Symbol('IAppLogic');
}
