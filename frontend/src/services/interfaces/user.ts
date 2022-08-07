import { interfaces } from 'inversify';

import { UserCreate, UserView } from '@/schemas/user';
import type { Response } from '@/types/service';

export interface IUserService {
  getCurrentUser: () => Promise<Response<UserView>>;
  login: (username: string, password: string) => Promise<Response<undefined>>;
  logged: () => Promise<Response<boolean>>;
  register: (userCreate: UserCreate) => Promise<Response<undefined>>;
}

export namespace IUserService {
  export const $: interfaces.ServiceIdentifier<IUserService> =
    Symbol('IUserService');
}
