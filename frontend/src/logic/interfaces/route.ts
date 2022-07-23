import { interfaces } from 'inversify';
import { Logic, LogicWrapper } from 'kea';

interface IRoute extends Logic {
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

export type IRouteLogic = LogicWrapper<IRoute>;

export namespace IRouteLogic {
  export const $: interfaces.ServiceIdentifier<IRouteLogic> =
    Symbol('IRouteLogic');
}
