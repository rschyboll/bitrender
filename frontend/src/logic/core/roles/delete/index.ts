import { kea, key, listeners, path, selectors } from 'kea';

import { connect, deps, requests } from '@/logic/builders';
import {
  IRoleUserCountLoaderLogic,
  IRoleViewLoaderLogic,
} from '@/logic/interfaces';
import { IRoleService } from '@/services/interfaces';

import { Listeners } from './listeners';
import { Selectors } from './selectors';
import type { RoleDeleteLogic } from './type';

export const roleDeleteLogic = kea<RoleDeleteLogic>([
  path(['roles', 'delete']),
  key((props) => props.id),
  deps((props) => ({
    roleService: IRoleService.$,
    roleViewLoaderLogic: {
      identifier: IRoleViewLoaderLogic.$,
      props: () => props,
    },
    roleUserCountLoaderLogic: {
      identifier: IRoleUserCountLoaderLogic.$,
      props: () => props,
    },
  })),
  connect(({ deps }) => [
    deps.roleViewLoaderLogic,
    deps.roleUserCountLoaderLogic,
  ]),
  requests(({ deps }) => ({
    delete: deps.roleService.delete,
  })),
  selectors(Selectors),
  listeners(Listeners),
]);
