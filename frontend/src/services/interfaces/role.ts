import type { interfaces } from "inversify";

import type { MRole } from "@/types/models";
import type { Response } from "@/services";

export interface IRoleService {
  getRoles: (
    input: MRole.Messages.GetRolesInput
  ) => Promise<Response<MRole.Messages.GetRolesOutput>>;
}

export namespace IRoleService {
  export const $: interfaces.ServiceIdentifier<IRoleService> =
    Symbol("IRoleService");
}
