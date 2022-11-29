import { afterMount, beforeUnmount, selectors } from 'kea';
import { actions, kea, listeners, path, reducers } from 'kea';

import { deps, requests } from '@/logic/builders';
import { IRoleService } from '@/services/interfaces';

import { Listeners } from './listeners';
import { Reducers } from './reducers';
import { Selectors } from './selectors';
import type { CreateRoleLogic } from './type';

export const roleCreateLogic = kea<CreateRoleLogic>([
  path(['roles', 'create']),
  deps({ roleService: IRoleService.$ }),
  actions({
    save: true,
    setName: (name) => ({ name }),
    setPermissionSelected: (permission, checked) => ({ permission, checked }),
    setDefault: (isDefault) => ({ isDefault }),
    setNameErrorMessage: (errorMessage) => ({ errorMessage }),
  }),
  requests(({ deps }) => ({
    create: deps.roleService.create,
  })),
  reducers(Reducers),
  selectors(Selectors),
  listeners(Listeners),
]);
