import { interfaces } from 'inversify';

import type { GetRolesInput, GetRolesOutput } from '@/services/messages/role';
import type { Response } from '@/types/service';

export interface IRoleService {
  getRoles: (input: GetRolesInput) => Promise<Response<GetRolesOutput>>;
}

export namespace IRoleService {
  export const $: interfaces.ServiceIdentifier<IRoleService> =
    Symbol('IRoleService');
}
