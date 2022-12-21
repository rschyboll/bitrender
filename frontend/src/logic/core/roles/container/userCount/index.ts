import { kea, path } from 'kea';

import config from '@/config';
import { container } from '@/logic/builders';

import type { RoleUserCountContainerLogic } from './type';

export const roleUserCountContainerLogic = kea<RoleUserCountContainerLogic>([
  path(['roles', 'container', 'userCount']),
  container({
    dataCleanTimeout: config.dataCleanTimeout,
    unmountDelay: config.containerUnmountDelay,
  }),
]);
