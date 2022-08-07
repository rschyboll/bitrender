import { actions, kea, listeners, reducers } from 'kea';
import { actionToUrl } from 'kea-router';
import { router } from 'kea-router';

import type { logicType } from './indexType';

const logic = kea<logicType>([
  actions({
    openApp: true,
    openRegisterPage: true,
    openLoginPage: () => ({
      currentPage: router.values.currentLocation.pathname,
    }),
    openUsersPage: true,
    openRolesPage: true,
    openErrorPage: true,
    returnToBeforeLogin: true,
  }),
  actionToUrl(() => ({
    openApp: () => `/app`,
    openLoginPage: () => '/login',
    openRegisterPage: () => '/register',
    openUsersPage: () => '/app/users',
    openRolesPage: () => '/app/roles',
    openErrorPage: () => '/error',
  })),
  reducers({
    beforeLoginPage: [
      null as null | string,
      {
        openLoginPage: (_, { currentPage }) => currentPage,
      },
    ],
  }),
  listeners(({ values }) => ({
    returnToBeforeLogin: () => {
      if (values.beforeLoginPage != null) {
        router.actions.replace(values.beforeLoginPage);
      } else {
        router.actions.replace('/app');
      }
    },
  })),
]);

export const routeLogic = logic;
