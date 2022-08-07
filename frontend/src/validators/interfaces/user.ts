import { interfaces } from 'inversify';

import { UserView } from '@/schemas/user';

export interface IUserValidators {
  validateUserView: (response: unknown) => response is UserView;
  mediumPasswordRegExp: RegExp;
  strongPasswordRegExp: RegExp;
  validateUserPasswordStrength: (password: string) => boolean;
  validateUserEmail: (email: string) => boolean;
}

export namespace IUserValidators {
  export const $: interfaces.ServiceIdentifier<IUserValidators> =
    Symbol('IUserValidators');
}
