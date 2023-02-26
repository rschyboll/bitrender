import { interfaces } from 'inversify';
import { LogicWrapper } from 'kea';

import { MakeOwnLogicType } from '@/logic/types/makeLogic';
import { RoleTableView } from '@/schemas/role';

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
  values: RoleTableView[];
}

export type IRolesTableLogic = LogicWrapper<
  MakeOwnLogicType<{
    actions: Actions;
    values: Values;
  }>
>;

export namespace IRolesTableLogic {
  export const $: interfaces.ServiceIdentifier<IRolesTableLogic> =
    Symbol('IRolesTableLogic');
}
