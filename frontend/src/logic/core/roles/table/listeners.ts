import type { ListenersDef } from '@/logic/types';

import type { RolesTableLogic } from './type';

export const Listeners: ListenersDef<RolesTableLogic> = ({
  actions,
  values,
  deps,
}) => ({
  refresh: async () => {
    actions.load();
  },
  load: async () => {
    const response = await deps.roleService.getRoles(values.listRequestInput);
    if (response.success) {
      actions.loadSuccess(response.data.items, response.data.rowCount);
    } else {
      actions.loadFailure();
    }
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
