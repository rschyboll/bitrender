import { interfaces } from 'inversify';
import { Logic, LogicWrapper } from 'kea';

import { RequestStatus } from '@/types/service';

interface ILogin extends Logic {
  readonly actions: {
    readonly login: (username: string, password: string) => void;
    readonly logout: () => void;
  };
  readonly values: {
    readonly loginStatus: RequestStatus;
    readonly loginErrorDetail: null | unknown;
    readonly logoutStatus: RequestStatus;
  };
}

export type ILoginLogic = LogicWrapper<ILogin>;

export namespace ILoginLogic {
  export const $: interfaces.ServiceIdentifier<ILoginLogic> =
    Symbol('ILoginLogic');
}
