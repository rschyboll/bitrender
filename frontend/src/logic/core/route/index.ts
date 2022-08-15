import {
  actions,
  afterMount,
  kea,
  listeners,
  path,
  props,
  reducers,
  sharedListeners,
} from 'kea';
import { actionToUrl, decodeParams } from 'kea-router';
import { router } from 'kea-router';
import { NavigateFunction } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

import Dependencies from '@/deps';
import { injectDepsToLogic } from '@/logic/utils';
import { history } from '@/pages/router';
import { IRouteValidators } from '@/validators/interfaces';

import type { logicType } from './indexType';

const logic = kea<logicType>([
  path(['route']),
  props(
    {} as {
      navigate: NavigateFunction;
      deps: {
        routeValidators: IRouteValidators;
      };
    },
  ),
  actions({
    openApp: true,
    openRegisterPage: true,
    openLoginPage: () => ({
      url: '/login',
      state: { lastPage: router.values.currentLocation.pathname },
    }),
    openVerifyPage: (email: string) => ({ email }),
    openUsersPage: true,
    openRolesPage: true,
    openErrorPage: true,
    returnToBeforeLogin: true,
  }),
  actionToUrl(() => ({
    openApp: () => `/app`,
    openRegisterPage: () => '/register',
    openVerifyPage: () => '/verify',
    openUsersPage: () => '/app/admin/users',
    openRolesPage: () => '/app/admin/roles',
    openErrorPage: () => '/error',
  })),
  reducers({
    verifyPageEmail: [null as null | string],
  }),
  sharedListeners(({ props }) => ({
    pushRoute: (payload: { url: string; state?: object }) => {
      history.push(payload.url, {
        ...payload.state,
        lastLocation: { ...history.location },
      });
    },
    replaceWithPrevious: () => {
      console.log(history.location.state);
    },
  })),
  listeners(({ sharedListeners }) => ({
    openLoginPage: sharedListeners.pushRoute,
    returnToBeforeLogin: sharedListeners.replaceWithPrevious,
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

export const routeLogic = injectDepsToLogic(logic, () => ({
  routeValidators: Dependencies.get(IRouteValidators.$),
}));
