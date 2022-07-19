import { actions, afterMount, kea, listeners, props, reducers } from 'kea';
import { actionToUrl, urlToAction } from 'kea-router';

import Dependencies from '@/deps';
import { injectDepsToLogic } from '@/logic/utils';
import { IUserService } from '@/services/interfaces';

import type { logicType } from './indexType';

const logic = kea<logicType>([
  props(
    {} as {
      deps: {
        userService: IUserService;
      };
    },
  ),
  actionToUrl(() => ({
    openApp: () => `/app`,
    openLoginPage: () => '/login',
    openRegisterPage: () => '/register',
    openUsersPage: () => '/app/users',
    openRolesPage: () => '/app/roles',
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
  }),
  reducers({}),
  listeners(({ props }) => ({
    loadCurrentUser: async () => {
      const me = await props.deps.userService.getCurrentUser();
      console.log(me);
    },
  })),
]);

export const appLogic = injectDepsToLogic(logic, () => ({
  userService: Dependencies.get(IUserService.$),
}));
