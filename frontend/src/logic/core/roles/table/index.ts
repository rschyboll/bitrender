import {
  actions,
  kea,
  listeners,
  path,
  props,
  reducers,
  selectors,
  sharedListeners,
} from 'kea';
import { subscriptions } from 'kea-subscriptions';

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
  reducers({
    localSearchString: [
      null as string | null,
      {
        setSearchString: (_, { searchString }) => searchString,
        setLocalSearchString: (_, { searchString }) => searchString,
      },
    ],
  }),
  actions({
    refresh: true,
    loadRecords: () => ({}),
    setLocalSearchString: (searchString: string) => ({ searchString }),
    setSearchString: (searchString: string) => ({ searchString }),
    setCurrentPage: (currentPage: number) => ({ currentPage }),
    setRowsPerPage: (rowsPerPage: number) => ({ rowsPerPage }),
  }),
  sharedListeners({
    loadRecords: async () => {},
  }),
  subscriptions(({ actions }) => ({
    searchString: (value, oldValue) => {
      if (oldValue == null && value != null) {
      }
    },
    rowsPerPage: (value, oldValue) => {
      if (value != null && oldValue != null) {
        console.log('ROWS PER PAGE CHANGED');
        console.log(value, oldValue);
      }
    },
    currentPage: (value, oldValue) => {},
  })),
  selectors(({ props }) => ({
    searchString: [
      () => [props.deps.routeLogic.selectors.hashParams],
      (hashParams) => {
        const search = hashParams['search'];
        if (typeof search == 'string') {
          return search;
        }
        return '';
      },
    ],
    rowsPerPage: [
      () => [props.deps.routeLogic.selectors.hashParams],
      (hashParams) => {
        const rows = hashParams['rows'];
        if (typeof rows == 'number') {
          return rows;
        }
        return 10;
      },
    ],
    currentPage: [
      () => [props.deps.routeLogic.selectors.hashParams],
      (hashParams) => {
        const page = hashParams['page'];
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
    setSearchString: async ({ searchString }, breakpoint) => {
      await breakpoint(250);
      props.deps.routeLogic.actions.openRolesPage(
        values.currentPage,
        values.rowsPerPage,
        searchString,
      );
    },
    setCurrentPage: ({ currentPage }) => {
      props.deps.routeLogic.actions.openRolesPage(
        currentPage,
        values.rowsPerPage,
        values.searchString,
      );
    },
    setRowsPerPage: ({ rowsPerPage }) => {
      props.deps.routeLogic.actions.openRolesPage(
        values.currentPage,
        rowsPerPage,
        values.searchString,
      );
    },
  })),
]);

export const rolesTableLogic = injectDepsToLogic(logic, () => ({
  routeLogic: Dependencies.get(IRouteLogic.$),
}));
