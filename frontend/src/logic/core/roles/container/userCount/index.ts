import { kea, path } from 'kea';

import { container } from '@/logic/builders';

import type { RoleUserCountContainerLogic } from './type';

export const roleUserCountContainerLogic = kea<RoleUserCountContainerLogic>([
  path(['roles', 'container', 'userCount']),
  container(),
]);
