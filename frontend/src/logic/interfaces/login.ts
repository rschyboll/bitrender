import { interfaces } from 'inversify';
import { Logic, LogicWrapper } from 'kea';

interface ILogin extends Logic {
  readonly actions: {
    readonly login: (username: string, password: string) => void;
    readonly logout: () => void;
  };
  readonly values: {
    readonly loginLoading: boolean;
    readonly loginSuccess: boolean;
    readonly loginFailure: boolean;
    readonly logoutLoading: boolean;
    readonly logoutSuccess: boolean;
    readonly logoutFailure: boolean;
  };
}

export type ILoginLogic = LogicWrapper<ILogin>;

export namespace ILoginLogic {
  export const $: interfaces.ServiceIdentifier<ILoginLogic> =
    Symbol('ILoginLogic');
}
