import {
  actions,
  beforeUnmount,
  kea,
  listeners,
  path,
  reducers,
  selectors,
} from 'kea';

import { IRoleConverters } from '@/converters/interfaces';
import { connect, deps, requests } from '@/logic/builders';
import { IRoleViewContainerLogic } from '@/logic/interfaces';
import { IRoleService } from '@/services/interfaces';

import { Listeners } from './listeners';
import { Reducers } from './reducers';
import { Selectors } from './selectors';
import type { RoleUserCountLoaderLogic } from './type';

export const roleUserCountLoaderLogic = kea<RoleUserCountLoaderLogic>([
  path(['roles', 'loader', 'table']),
  deps({
    roleViewContainerLogic: IRoleViewContainerLogic.$,
    roleConverters: IRoleConverters.$,
    roleService: IRoleService.$,
  }),
  connect(({ deps }) => [deps.roleViewContainerLogic]),
  actions({
    setLoadedEntryIds: (entryIds) => ({ entryIds }),
    setEntryRowCount: (rowCount) => ({ rowCount }),
  }),
  requests(({ deps }) => ({ load: deps.roleService.getTable })),
  reducers(Reducers),
  selectors(Selectors),
  listeners(Listeners),
  beforeUnmount(({ deps, values }) => {
    deps.roleViewContainerLogic.actions.releaseEntries(values.loadedEntryIds);
  }),
]);
