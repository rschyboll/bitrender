import type { ListenersDef } from '@/logic/types';

import type { RolesTableLogic } from './type';

export const Listeners: ListenersDef<RolesTableLogic> = ({ values, deps }) => ({
  refresh: async () => {
    deps.roleTableLoaderLogic.actions.load(values.listRequestInput);
  },
  setSearchString: async ({ searchString }, breakpoint) => {
    await breakpoint(250);
    deps.routeLogic.actions.openRolesPage(
      values.currentPage,
      values.rowsPerPage,
      searchString,
    );
  },
  setCurrentPage: ({ currentPage }) => {
    deps.routeLogic.actions.openRolesPage(
      currentPage,
      values.rowsPerPage,
      values.searchString,
    );
  },
  setRowsPerPage: ({ rowsPerPage }) => {
    deps.routeLogic.actions.openRolesPage(
      values.currentPage,
      rowsPerPage,
      values.searchString,
    );
  },
});
