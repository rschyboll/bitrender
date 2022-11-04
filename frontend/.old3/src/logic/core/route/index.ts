import { deepEqual } from 'fast-equals';
import { Path } from 'history';
import { Location } from 'history';
import {
  actions,
  afterMount,
  kea,
  listeners,
  path,
  props,
  reducers,
  selectors,
  sharedListeners,
} from 'kea';
import { decodeParams } from 'kea-router';

import Dependencies from '@/deps';
import { injectDepsToLogic } from '@/logic/utils';
import { history } from '@/pages/router';
import { IRouteValidators } from '@/validators/interfaces';

import type { logicType } from './indexType';

const logic = kea<logicType>([
  path(['route']),
  props(
    {} as {
      deps: {
        routeValidators: IRouteValidators;
      };
    },
  ),
  reducers(() => ({
    currentLocation: [
      { ...history.location },
      {
        updateLocationState: (_, { location }) => {
          console.log('REDUCER');
          console.log(location.hash);
          return { ...location };
        },
      },
    ],
  })),
  selectors({
    pathname: [
      (selectors) => [selectors.currentLocation],
      (currentLocation) => {
        return currentLocation.pathname;
      },
    ],
    search: [
      (selectors) => [selectors.currentLocation],
      (currentLocation) => {
        return currentLocation.search;
      },
    ],
    hash: [
      (selectors) => [selectors.currentLocation],
      (currentLocation) => {
        return currentLocation.hash;
      },
    ],
    state: [
      (selectors) => [selectors.currentLocation],
      (currentLocation) => {
        return currentLocation.state;
      },
    ],
    key: [
      (selectors) => [selectors.currentLocation],
      (currentLocation) => {
        return currentLocation.key;
      },
    ],
    searchParams: [
      (selectors) => [selectors.search],
      (search) => {
        return decodeParams(search, '?') as Record<string, unknown>;
      },
    ],
    hashParams: [
      (selectors) => [selectors.hash],
      (hash) => {
        return decodeParams(hash, '#') as Record<string, unknown>;
      },
    ],
  }),
  actions({
    updateLocationState: (location: Location) => ({ location }),
    openRoute: (to: string | Partial<Path>, state?: object) => ({
      to: to,
      state: state,
    }),
    replaceRoute: (to: string | Partial<Path>, state?: object) => ({
      to: to,
      state: state,
    }),
    openApp: () => ({
      to: '/app',
    }),
    openRegisterPage: () => ({
      to: '/register',
    }),
    openLoginPage: () => ({
      to: '/login',
    }),
    openVerifyPage: (email: string) => ({
      to: '/login',
      state: { verifyEmail: email },
    }),
    openUsersPage: () => ({
      to: '/app/admin/users',
    }),
    openRolesPage: (
      page = 0,
      rows = 10,
      search = null,
    ): { to: Partial<Path> } => ({
      to: {
        pathname: `/app/admin/roles`,
        hash: `page=${page}&rows=${rows}${
          search != null && search != '' ? `&search=${search}` : ''
        }`,
      },
    }),
    openErrorPage: () => ({
      to: '/error',
    }),
    returnToBeforeLogin: true,
  }),
  sharedListeners(({ props }) => ({
    pushRoute: (payload: { to: string | Partial<Path>; state?: object }) => {
      history.push(payload.to, {
        ...payload.state,
        lastLocation: { ...history.location },
      });
    },
    replaceRoute: (payload: { to: string | Partial<Path>; state?: object }) => {
      if (
        props.deps.routeValidators.stateHasLastLocation(history.location.state)
      ) {
        history.replace(payload.to, {
          ...payload.state,
          lastLocation: { ...history.location.state.lastLocation },
        });
      } else {
        history.replace(payload.to, {
          ...payload.state,
        });
      }
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
    openRoute: sharedListeners.pushRoute,
    replaceRoute: sharedListeners.replaceRoute,
    openApp: sharedListeners.pushRoute,
    openRegisterPage: sharedListeners.pushRoute,
    openLoginPage: sharedListeners.pushRoute,
    openVerifyPage: sharedListeners.pushRoute,
    openUsersPage: sharedListeners.pushRoute,
    openRolesPage: sharedListeners.pushRoute,
    openErrorPage: sharedListeners.pushRoute,
    returnToBeforeLogin: sharedListeners.replaceWithPrevious,
  })),
  afterMount(({ actions, values }) => {
    history.listen((update) => {
      if (!deepEqual(update.location, values.currentLocation)) {
        actions.updateLocationState(update.location);
      }
    });
  }),
]);

export const routeLogic = injectDepsToLogic(logic, () => ({
  routeValidators: Dependencies.get(IRouteValidators.$),
}));
