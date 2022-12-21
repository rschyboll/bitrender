import {
  beforeUnmount,
  events,
  kea,
  key,
  listeners,
  path,
  selectors,
} from 'kea';
import { subscriptions } from 'kea-subscriptions';

import { connect, deps, requests } from '@/logic/builders';
import { IRoleUserCountContainerLogic } from '@/logic/interfaces';
import { IRoleService } from '@/services/interfaces';

import { Listeners } from './listeners';
import { Selectors } from './selectors';
import { Subscriptions } from './subscriptions';
import type { RoleUserCountLoaderLogic } from './type';

export const roleUserCountLoaderLogic = kea<RoleUserCountLoaderLogic>([
  path(['roles', 'loader', 'userCount']),
  key((props) => props.id),
  deps({
    roleUserCountContainerLogic: IRoleUserCountContainerLogic.$,
    roleService: IRoleService.$,
  }),
  connect(({ deps }) => [deps.roleUserCountContainerLogic]),
  requests(({ deps }) => ({ load: deps.roleService.getUserCount })),
  selectors(Selectors),
  listeners(Listeners),
  subscriptions(Subscriptions),
  beforeUnmount(({ deps, values }) => {
    deps.roleUserCountContainerLogic.actions.releaseEntries([values.id]);
  }),
]);
