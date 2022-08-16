import { interfaces } from 'inversify';
import { Logic, LogicWrapper } from 'kea';
import { To } from 'react-router-dom';

interface IRoute extends Logic {
  readonly actions: {
    readonly openRoute: (to: To, state?: object) => void;
    readonly replaceRoute: (to: To, state?: object) => void;
    readonly openApp: () => void;
    readonly openLoginPage: () => void;
    readonly openRegisterPage: () => void;
    readonly openVerifyPage: (email: string) => void;
    readonly openUsersPage: () => void;
    readonly openRolesPage: () => void;
    readonly openErrorPage: () => void;
    readonly returnToBeforeLogin: () => void;
  };
  readonly values: {};
}

export type IRouteLogic = LogicWrapper<IRoute>;

export namespace IRouteLogic {
  export const $: interfaces.ServiceIdentifier<IRouteLogic> =
    Symbol('IRouteLogic');
}
