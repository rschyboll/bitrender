import { actions, kea, listeners, path, reducers } from 'kea';

import { connect, requests } from '@/logic/builders';

import { Listeners } from './listeners';
import { Reducers } from './reducers';
import type { RoleTableLoaderLogic } from './type';

export const rolesTableLoaderLogic = kea<RoleTableLoaderLogic>([
  path(['roles', 'loader', 'table']),
  connect(({ deps }) => [deps.roleViewContainerLogic]),
  actions({
    setLoadedEntryIds: (entryIds) => ({ entryIds }),
    setEntryRowCount: (rowCount) => ({ rowCount }),
  }),
  requests(({ deps }) => ({ load: deps.roleService.getTable })),
  reducers(Reducers),
  listeners(Listeners),
]);
