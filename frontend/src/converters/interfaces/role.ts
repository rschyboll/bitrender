import type { interfaces } from "inversify";

import type { MRole } from "@/types/models";

export interface IRoleConverters {
  viewToTableView: (view: MRole.View) => MRole.TableView;
}

export namespace IRoleConverters {
  export const $: interfaces.ServiceIdentifier<IRoleConverters> =
    Symbol("IRoleConverters");
}
