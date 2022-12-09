import { kea, key, listeners, path, reducers } from 'kea';

import { connect, deps } from '@/logic/builders';
import { IRoleViewLoaderLogic } from '@/logic/interfaces';
import { IRoleService } from '@/services/interfaces';

import { Listeners } from './listeners';
import { Reducers } from './reducers';
import type { RoleUpdateLogic } from './type';

export const roleUpdateLogic = kea<RoleUpdateLogic>([
  path(['roles', 'update']),
  key((props) => props.id),
  deps(({ props }) => ({
    roleService: IRoleService.$,
    roleViewLoaderLogic: {
      identifier: IRoleViewLoaderLogic.$,
      props: () => props,
    },
    objectViewLoaderLogic: {
      identifier: IRoleViewLoaderLogic.$,
      props: () => props,
    },
  })),
  connect(({ deps }) => [deps.roleViewLoaderLogic]),
  reducers(Reducers),
  listeners(Listeners),
]);
