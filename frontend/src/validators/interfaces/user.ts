import { interfaces } from 'inversify';

import { UserViewResponse } from '@/types/user';

export interface IUserValidators {
  validateUserViewResponse: (response: unknown) => response is UserViewResponse;
}

export namespace IUserValidators {
  export const $: interfaces.ServiceIdentifier<IUserValidators> =
    Symbol('IUserValidators');
}
