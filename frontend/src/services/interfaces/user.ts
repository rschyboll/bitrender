import { interfaces } from 'inversify';

import type { Response } from '@/services';
import { UserView } from '@/types/user';

export interface IUserService {
  getMe: () => Promise<Response<UserView>>;
}

export namespace IUserService {
  export const $: interfaces.ServiceIdentifier<IUserService> =
    Symbol('IUserService');
}
