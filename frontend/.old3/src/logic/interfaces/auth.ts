import { interfaces } from 'inversify';
import { Logic, LogicWrapper } from 'kea';

import { RequestStatus } from '@/types/service';

interface IAuth extends Logic {
  readonly actions: {
    readonly checkLoggedIn: () => void;
    readonly login: (username: string, password: string) => void;
    readonly logout: () => void;
    readonly register: (
      email: string,
      username: string,
      password: string,
    ) => void;
  };
  readonly values: {
    readonly loginStatus: RequestStatus;
    readonly loginErrorDetail: null | unknown;
    readonly logoutStatus: RequestStatus;
    readonly registerStatus: RequestStatus;
    readonly registerWeakPassword: boolean;
    readonly registerWrongEmail: boolean;
    readonly registerErrorDetail: null | unknown;
  };
}

export type IAuthLogic = LogicWrapper<IAuth>;

export namespace IAuthLogic {
  export const $: interfaces.ServiceIdentifier<IAuthLogic> =
    Symbol('IAuthLogic');
}
