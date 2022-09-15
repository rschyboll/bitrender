import { interfaces } from 'inversify';
import { Logic, LogicWrapper } from 'kea';

interface IRolesTable extends Logic {
  readonly actions: {
    setSearchString: (searchString: string) => void;
    setCurrentPage: (currentPage: number) => void;
    setRowsPerPage: (rowsPerPage: number) => void;
  };
  readonly values: {
    localSearchString: string | null;
    searchString: string | null;
    currentPage: number;
    rowsPerPage: number;
    amountOfRecords: number | null;
  };
}

export type IRolesTableLogic = LogicWrapper<IRolesTable>;

export namespace IRolesTableLogic {
  export const $: interfaces.ServiceIdentifier<IRolesTableLogic> =
    Symbol('IRolesTableLogic');
}
