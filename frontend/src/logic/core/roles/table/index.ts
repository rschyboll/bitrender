import { actions, kea, listeners, path, reducers, selectors } from 'kea';
import { subscriptions } from 'kea-subscriptions';

import { connect, deps } from '@/logic/builders';
import { IRoleTableLoaderLogic, IRouteLogic } from '@/logic/interfaces';

import { Listeners } from './listeners';
import { Reducers } from './reducers';
import { Selectors } from './selectors';
import { Subscriptions } from './subscriptions';
import type { RolesTableLogic } from './type';

export const rolesTableLogic = kea<RolesTableLogic>([
  path(['roles', 'table']),
  deps({
    routeLogic: IRouteLogic.$,
    roleTableLoaderLogic: IRoleTableLoaderLogic.$,
  }),
  connect(({ deps }) => [deps.roleTableLoaderLogic]),
  actions({
    refresh: true,
    setSearchString: (searchString) => ({ searchString }),
    setCurrentPage: (currentPage) => ({ currentPage }),
    setLocalSearchString: (searchString) => ({ searchString }),
    setRowsPerPage: (rowsPerPage) => ({ rowsPerPage }),
  }),
  reducers(Reducers),
  selectors(Selectors),
  listeners(Listeners),
  subscriptions(Subscriptions),
]);
