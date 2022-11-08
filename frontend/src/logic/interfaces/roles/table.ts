import type { interfaces } from "inversify";
import type { LogicWrapper } from "kea";

import type { MakeOwnLogicType } from "@/logic/types/makeLogic";
import type { MRole } from "@/types/models";

interface Actions {
  setSearchString: (searchString: string) => void;
  setCurrentPage: (currentPage: number) => void;
  setRowsPerPage: (rowsPerPage: number) => void;
}

interface Values {
  searchString: string | null;
  currentPage: number;
  rowsPerPage: number;
  amountOfRecords: number | null;
  values: MRole.TableView[];
}

export type IRolesTableLogic = LogicWrapper<
  MakeOwnLogicType<{
    actions: Actions;
    values: Values;
  }>
>;

export namespace IRolesTableLogic {
  export const $: interfaces.ServiceIdentifier<IRolesTableLogic> =
    Symbol("IRolesTableLogic");
}
