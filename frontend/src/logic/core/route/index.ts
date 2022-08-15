import { actions, kea, listeners, path, props, sharedListeners } from 'kea';
import { NavigateFunction } from 'react-router-dom';

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
    openApp: () => ({
      url: '/app',
    }),
    openRegisterPage: () => ({
      url: '/register',
    }),
    openLoginPage: () => ({
      url: '/login',
    }),
    openVerifyPage: (email: string) => ({
      url: '/login',
      state: { verifyEmail: email },
    }),
    openUsersPage: () => ({
      url: '/app/admin/users',
    }),
    openRolesPage: () => ({
      url: '/app/admin/roles',
    }),
    openErrorPage: () => ({
      url: '/error',
    }),
    returnToBeforeLogin: true,
  }),
  sharedListeners(({ props }) => ({
    pushRoute: (payload: { url: string; state?: object }) => {
      history.push(payload.url, {
        ...payload.state,
        lastLocation: { ...history.location },
      });
    },
    replaceWithPrevious: () => {
      if (
        props.deps.routeValidators.stateHasLastLocation(history.location.state)
      ) {
        history.replace(
          history.location.state.lastLocation.pathname,
          history.location.state.lastLocation.state,
        );
      } else {
        history.replace('/app');
      }
    },
  })),
  listeners(({ sharedListeners }) => ({
    openApp: sharedListeners.pushRoute,
    openRegisterPage: sharedListeners.pushRoute,
    openLoginPage: sharedListeners.pushRoute,
    openVerifyPage: sharedListeners.pushRoute,
    openUsersPage: sharedListeners.pushRoute,
    openRolesPage: sharedListeners.pushRoute,
    openErrorPage: sharedListeners.pushRoute,
    returnToBeforeLogin: sharedListeners.replaceWithPrevious,
  })),
]);

export const routeLogic = injectDepsToLogic(logic, () => ({
  routeValidators: Dependencies.get(IRouteValidators.$),
}));
