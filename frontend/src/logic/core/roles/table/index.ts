import { actions, kea, listeners, path, props, reducers, selectors } from 'kea';

import Dependencies from '@/deps';
import { IRouteLogic } from '@/logic/interfaces';
import { injectDepsToLogic } from '@/logic/utils';

import type { logicType } from './indexType';

const logic = kea<logicType>([
  path(['roles', 'table']),
  props(
    {} as {
      deps: {
        routeLogic: IRouteLogic;
      };
    },
  ),
  actions({
    setCurrentPage: (currentPage: number) => ({ currentPage }),
    setRowsPerPage: (rowsPerPage: number) => ({ rowsPerPage }),
  }),
  selectors(({ props }) => ({
    rowsPerPage: [
      () => [props.deps.routeLogic.selectors.searchParams],
      (searchParams) => {
        const rows = searchParams['rows'];
        console.log(rows);
        if (typeof rows == 'number') {
          return rows;
        }
        return 10;
      },
    ],
    currentPage: [
      () => [props.deps.routeLogic.selectors.searchParams],
      (searchParams) => {
        const page = searchParams['page'];
        if (typeof page == 'number') {
          return page;
        }
        return 0;
      },
    ],
  })),
  reducers({
    amountOfRecords: [100 as number | null],
  }),
  listeners(({ props, values }) => ({
    setCurrentPage: ({ currentPage }) => {
      props.deps.routeLogic.actions.openRolesPage(
        currentPage,
        values.rowsPerPage,
      );
    },
    setRowsPerPage: ({ rowsPerPage }) => {
      props.deps.routeLogic.actions.openRolesPage(
        values.currentPage,
        rowsPerPage,
      );
    },
  })),
]);

export const rolesTableLogic = injectDepsToLogic(logic, () => ({
  routeLogic: Dependencies.get(IRouteLogic.$),
}));
