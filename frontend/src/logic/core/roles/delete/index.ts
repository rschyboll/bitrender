import { actions, kea, listeners, path, selectors } from 'kea';

import { deps, requests } from '@/logic/builders';
import { IRoleService } from '@/services/interfaces';

import { Listeners } from './listeners';
import { Selectors } from './selectors';
import type { RoleCreateLogic } from './type';

export const roleCreateLogic = kea<RoleCreateLogic>([
  path(['roles', 'create']),
  deps({ roleService: IRoleService.$ }),
  actions({}),
  requests(({ deps }) => ({
    create: deps.roleService.create,
  })),
  selectors(Selectors),
  listeners(Listeners),
]);
