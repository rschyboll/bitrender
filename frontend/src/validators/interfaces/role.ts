import type { interfaces } from 'inversify';

import type { MRole } from '@/types/models';

export interface IRoleValidators {
  validateGetListOutput: (
    value: unknown,
  ) => value is MRole.Messages.GetListOutput;
  validateCreateOutput: (
    value: unknown,
  ) => value is MRole.Messages.CreateOutput;
  isPermission: (value: unknown) => value is MRole.Permission;
}

export namespace IRoleValidators {
  export const $: interfaces.ServiceIdentifier<IRoleValidators> =
    Symbol('IRoleValidators');
}
