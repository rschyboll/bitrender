import { actions, afterMount, kea, reducers } from 'kea';
import { actionToUrl } from 'kea-router';

import type { logicType } from './indexType';

const logic = kea<logicType>([
  actions({
    openApp: true,
    openRegisterPage: true,
    openLoginPage: () => {
      console.log('TESTHMM');
    },
    openUsersPage: true,
    openRolesPage: true,
    openErrorPage: true,
  }),
  actionToUrl(() => ({
    openApp: () => `/app`,
    openLoginPage: () => {
      console.log('LOGIN');
      return '/login';
    },
    openRegisterPage: () => '/register',
    openUsersPage: () => '/app/users',
    openRolesPage: () => '/app/roles',
    openErrorPage: () => '/error',
  })),
]);

export const routeLogic = logic;
