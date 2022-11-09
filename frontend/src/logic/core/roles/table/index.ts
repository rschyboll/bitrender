import {
  actions,
  afterMount,
  kea,
  listeners,
  path,
  reducers,
  selectors,
} from 'kea';
import { subscriptions } from 'kea-subscriptions';

import { IRoleConverters } from '@/converters/interfaces';
import { deps } from '@/logic/builders';
import { IRouteLogic } from '@/logic/interfaces';
import { IRoleService } from '@/services/interfaces';

import { Listeners } from './listeners';
import { Reducers } from './reducers';
import { Selectors } from './selectors';
import { Subscriptions } from './subscriptions';
import type { RolesTableLogic } from './type';

export const rolesTableLogic = kea<RolesTableLogic>([
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
  selectors(Selectors),
  listeners(Listeners),
  subscriptions(Subscriptions),
  afterMount(({ actions }) => {
    actions.refresh();
  }),
]);
