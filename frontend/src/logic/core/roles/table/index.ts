import {
  actions,
  afterMount,
  kea,
  listeners,
  path,
  props,
  reducers,
  selectors,
} from 'kea';
import { subscriptions } from 'kea-subscriptions';

import { IRoleConverters } from '@/converters/interfaces';
import Dependencies from '@/deps';
import { deps } from '@/logic/builders';
import { IRouteLogic } from '@/logic/interfaces';
import { injectDepsToLogic } from '@/logic/utils';
import { RequestStatus } from '@/services';
import { IRoleService } from '@/services/interfaces';
import { ListRequestInput, SearchRule } from '@/services/messages/list';
import { LoadState } from '@/types';

import { Reducers } from './reducers';
import type { RolesTableLogic } from './type';

const logic = kea<RolesTableLogic>([
  path(['roles', 'table']),
  deps({
    roleConverters: IRoleConverters.$,
    roleService: IRoleService.$,
    routeLogic: IRouteLogic.$,
  }),
  actions({
    refresh: true,
    load: true,
    loadSuccess: (roles, rowCount) => ({
      roles,
      rowCount,
    }),
    loadFailure: true,
    setSearchString: (searchString) => ({ searchString }),
    setCurrentPage: (currentPage) => ({ currentPage }),
    setLocalSearchString: (searchString) => ({ searchString }),
    setRowsPerPage: (rowsPerPage) => ({ rowsPerPage }),
  }),
  reducers(Reducers),
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
  selectors(({ props }) => ({})),
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
  roleConverters: Dependencies.get(IRoleConverters.$),
}));
