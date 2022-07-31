import { actions, afterMount, kea, reducers } from 'kea';
import { actionToUrl } from 'kea-router';

import type { logicType } from './indexType';

const logic = kea<logicType>([
  actions({
    openApp: true,
    openRegisterPage: true,
    openLoginPage: true,
    openUsersPage: true,
    openRolesPage: true,
    openErrorPage: true,
    replaceWithPrevious: true,
  }),
  actionToUrl(() => ({
    openApp: () => `/app`,
    openLoginPage: () => '/login',
    openRegisterPage: () => '/register',
    openUsersPage: () => '/app/users',
    openRolesPage: () => '/app/roles',
    openErrorPage: () => '/error',
  })),
]);

export const routeLogic = logic;
