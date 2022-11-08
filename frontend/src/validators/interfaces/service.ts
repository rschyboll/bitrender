import { interfaces } from "inversify";

import { ApiError } from "@/services/types";

export interface IServiceValidators {
  validateHttpError: (response: unknown) => response is ApiError;
}

export namespace IServiceValidators {
  export const $: interfaces.ServiceIdentifier<IServiceValidators> =
    Symbol("IServiceValidators");
}
