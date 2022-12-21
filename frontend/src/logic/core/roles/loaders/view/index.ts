import {
  actions,
  afterMount,
  beforeUnmount,
  kea,
  key,
  listeners,
  path,
  selectors,
} from 'kea';
import { subscriptions } from 'kea-subscriptions';

import { connect, deps, requests } from '@/logic/builders';
import { IRoleViewContainerLogic } from '@/logic/interfaces';
import { IRoleService } from '@/services/interfaces';

import { Listeners } from './listeners';
import { Selectors } from './selectors';
import { Subscriptions } from './subscriptions';
import type { RoleViewLoaderLogic } from './type';

export const roleViewLoaderLogic = kea<RoleViewLoaderLogic>([
  path(['roles', 'loader', 'view']),
  key((props) => props.id),
  deps({
    roleService: IRoleService.$,
    roleViewContainerLogic: IRoleViewContainerLogic.$,
  }),
  connect(({ deps }) => [deps.roleViewContainerLogic]),
  actions({
    refresh: true,
  }),
  requests(({ deps }) => ({
    load: deps.roleService.getById,
  })),
  selectors(Selectors),
  listeners(Listeners),
  subscriptions(Subscriptions),
  afterMount(({ deps, values }) => {
    if (values.entry != null) {
      deps.roleViewContainerLogic.actions.useEntries([values.entry.id]);
    }
  }),
  beforeUnmount(({ deps, values }) => {
    deps.roleViewContainerLogic.actions.releaseEntries([values.id]);
  }),
]);
