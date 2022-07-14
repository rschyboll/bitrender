import { interfaces } from 'inversify';

import type { Response } from '@/types/service';
import { UserView } from '@/types/user';

export interface IUserService {
  getCurrentUser: () => Promise<Response<UserView>>;
}

export namespace IUserService {
  export const $: interfaces.ServiceIdentifier<IUserService> =
    Symbol('IUserService');
}
