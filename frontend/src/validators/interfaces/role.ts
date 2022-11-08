import type { interfaces } from "inversify";

import type { MRole } from "@/types/models";

export interface IRoleValidators {
  validateGetRolesOutput: (
    value: unknown
  ) => value is MRole.Messages.GetRolesOutput;
}

export namespace IRoleValidators {
  export const $: interfaces.ServiceIdentifier<IRoleValidators> =
    Symbol("IRoleValidators");
}
