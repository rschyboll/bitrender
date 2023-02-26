import { interfaces } from 'inversify';

import { GetRolesOutput } from '@/services/messages/role';

export interface IRoleValidators {
  validateGetRolesOutput: (value: unknown) => value is GetRolesOutput;
}

export namespace IRoleValidators {
  export const $: interfaces.ServiceIdentifier<IRoleValidators> =
    Symbol('IRoleValidators');
}
