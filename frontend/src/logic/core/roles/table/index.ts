import {
  actions,
  afterMount,
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
import { RoleColumns, RoleView } from '@/schemas/role';
import { IRoleService } from '@/services/interfaces';
import { ListRequestInput, SearchRule } from '@/services/messages/list';
import { LoadState } from '@/types';

import type { logicType } from './indexType';

const logic = kea<logicType>([
  path(['roles', 'table']),
  props(
    {} as {
      deps: {
        routeLogic: IRouteLogic;
        roleService: IRoleService;
      };
    },
  ),
  reducers({
    localSearchString: [
      null as string | null,
      {
        setSearchString: (_, { searchString }) => searchString,
      },
    ],
    loadState: [
      LoadState.Idle as LoadState,
      {
        load: () => LoadState.InProgress,
        loadSuccess: () => LoadState.Idle,
        loadFailure: () => LoadState.Failure,
      },
    ],
    values: [
      [] as RoleView[],
      {
        loadSuccess: (_, { roles }) => roles,
      },
    ],
  }),
  actions({
    refresh: true,
    setSearchString: (searchString: string) => ({ searchString }),
    setCurrentPage: (currentPage: number) => ({ currentPage }),
    setLocalSearchString: (searchString: string) => ({ searchString }),
    setRowsPerPage: (rowsPerPage: number) => ({ rowsPerPage }),
    load: true,
    loadSuccess: (roles: RoleView[], row_count: number) => ({
      roles,
      row_count,
    }),
    loadFailure: true,
  }),
  subscriptions(({ actions, values }) => ({
    listRequestInput: async () => {
      actions.refresh();
    },
    urlSearchString: (value) => {
      if (value != values.localSearchString) {
        actions.setLocalSearchString(value);
      }
    },
  })),
  selectors(({ props }) => ({
    searchString: [
      (selectors) => [selectors.urlSearchString, selectors.localSearchString],
      (urlSearchString, localSearchString) => {
        if (localSearchString == null) {
          return urlSearchString;
        }
        return localSearchString;
      },
    ],
    urlSearchString: [
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
    listRequestInput: [
      (selectors) => [
        selectors.currentPage,
        selectors.rowsPerPage,
        selectors.urlSearchString,
      ],
      (currentPage, rowsPerPage, searchString) => {
        const listRequestInput: ListRequestInput<RoleColumns> = {
          search: [
            {
              column: 'name',
              rule: SearchRule.CONTAINS,
              value: searchString,
            },
          ],
          page: {
            pageNr: currentPage,
            recordsPerPage: rowsPerPage,
          },
        };
        return listRequestInput;
      },
    ],
  })),
  reducers({
    amountOfRecords: [
      0 as number,
      {
        loadSuccess: (_, { row_count }) => row_count,
      },
    ],
  }),
  listeners(({ props, values, actions }) => ({
    refresh: async () => {
      actions.load();
    },
    load: async () => {
      const response = await props.deps.roleService.getRoles(
        values.listRequestInput,
      );
      if (response.success) {
        actions.loadSuccess(response.data.items, response.data.rowCount);
      } else {
        actions.loadFailure();
      }
    },
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
        values.urlSearchString,
      );
    },
    setRowsPerPage: ({ rowsPerPage }) => {
      props.deps.routeLogic.actions.openRolesPage(
        values.currentPage,
        rowsPerPage,
        values.urlSearchString,
      );
    },
  })),
  afterMount(({ actions }) => {
    actions.refresh();
  }),
]);

export const rolesTableLogic = injectDepsToLogic(logic, () => ({
  routeLogic: Dependencies.get(IRouteLogic.$),
  roleService: Dependencies.get(IRoleService.$),
}));
