import { actions, kea } from 'kea';
import { actionToUrl, urlToAction } from 'kea-router';

import { injectDepsToLogic } from '@/logic/utils';

import type { logicType } from './indexType';

const logic = kea<logicType>([
  actionToUrl(() => ({
    openApp: () => `/app`,
    openLoginPage: () => '/login',
    openRegisterPage: () => '/register',
    openUsersPage: () => '/app/users',
    openRolesPage: () => '/app/roles',
    openErrorPage: () => '/error',
  })),
  urlToAction(({ actions }) => ({
    '/app/users': () => actions.loadCurrentUser(),
    '/app/roles': () => actions.loadCurrentUser(),
  })),
  actions({
    loadCurrentUser: true,
    openApp: true,
    openLoginPage: true,
    openRegisterPage: true,
    openUsersPage: true,
    openRolesPage: true,
    openErrorPage: true,
  }),
]);

export const routeLogic = injectDepsToLogic(logic, () => ({}));
