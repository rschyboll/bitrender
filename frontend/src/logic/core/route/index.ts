import { actions, afterMount, kea, listeners, path, reducers } from 'kea';
import { actionToUrl, decodeParams } from 'kea-router';
import { router } from 'kea-router';

import { history } from '@/pages/router';

import type { logicType } from './indexType';

const logic = kea<logicType>([
  path(['route']),
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
    openUsersPage: () => '/app/admin/users',
    openRolesPage: () => '/app/admin/roles',
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
  afterMount(() => {
    history.listen((update) => {
      if (
        update.location.pathname != router.values.location.pathname ||
        update.location.search != router.values.location.search ||
        update.location.hash != router.values.location.hash
      ) {
        router.actions.locationChanged({
          method: update.action,
          ...update.location,
          url: update.location.pathname,
          hashParams: decodeParams(update.location.hash),
          searchParams: decodeParams(update.location.search),
        });
      }
    });
  }),
]);

export const routeLogic = logic;
