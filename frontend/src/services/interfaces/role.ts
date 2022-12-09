import type { interfaces } from 'inversify';

import type { Response } from '@/services';
import type { MRole } from '@/types/models';

export interface IRoleService {
  getTable: (
    input: MRole.Messages.GetListInput,
  ) => Promise<Response<MRole.Messages.GetListOutput>>;
  create: (
    input: MRole.Messages.CreateInput,
  ) => Promise<Response<MRole.Messages.CreateOutput>>;
  getById: (
    input: MRole.Messages.GetByIdInput,
  ) => Promise<Response<MRole.Messages.GetByIdOutput>>;
}

export namespace IRoleService {
  export const $: interfaces.ServiceIdentifier<IRoleService> =
    Symbol('IRoleService');
}
