import { actions, kea, listeners, path, reducers } from 'kea';

import { deps, requests } from '@/logic/builders';
import { IRoleService } from '@/services/interfaces';

import { Listeners } from './listeners';
import { Reducers } from './reducers';
import type { CreateRoleLogic } from './type';

export const createRoleLogic = kea<CreateRoleLogic>([
  path(['roles', 'create']),
  deps({ roleService: IRoleService.$ }),
  actions({
    setName: (name) => ({ name }),
    setPermissionSelected: (permission, checked) => ({ permission, checked }),
    setDefault: (isDefault) => ({ isDefault }),
  }),
  requests(({ deps }) => ({
    create: deps.roleService.create,
  })),
  reducers(Reducers),
  listeners(Listeners),
]);
