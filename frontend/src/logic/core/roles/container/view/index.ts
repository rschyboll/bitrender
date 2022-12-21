import { kea, path } from 'kea';

import config from '@/config';
import { container } from '@/logic/builders';

import type { RoleViewContainerLogic } from './type';

export const roleViewContainerLogic = kea<RoleViewContainerLogic>([
  path(['roles', 'container', 'view']),
  container({
    dataCleanTimeout: config.dataCleanTimeout,
    unmountDelay: config.containerUnmountDelay,
  }),
]);
