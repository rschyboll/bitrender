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
    readonly openRolesPage: (
      page?: number,
      rows?: number,
      search?: string,
    ) => void;
    readonly openErrorPage: () => void;
    readonly returnToBeforeLogin: () => void;
  };
  readonly values: {
    readonly searchParams: Record<string, unknown>;
  };
  readonly selectors: {
    readonly searchParams: (
      state: unknown,
      props?: unknown,
    ) => Record<string, unknown>;
    readonly hashParams: (
      state: unknown,
      props?: unknown,
    ) => Record<string, unknown>;
  };
}

export type IRouteLogic = LogicWrapper<IRoute>;

export namespace IRouteLogic {
  export const $: interfaces.ServiceIdentifier<IRouteLogic> =
    Symbol('IRouteLogic');
}
