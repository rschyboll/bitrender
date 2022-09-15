import { Path } from 'history';
import {
  actions,
  afterMount,
  kea,
  listeners,
  path,
  props,
  selectors,
  sharedListeners,
} from 'kea';
import { combineUrl, decodeParams, router } from 'kea-router';

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
  reducers({
    hashParams: [{} as Record<string, any>],
  }),
  actions({
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
      console.log('PUSH ROUTE');
    },
    replaceRoute: (payload: { to: string | Partial<Path>; state?: object }) => {
      if (
        props.deps.routeValidators.stateHasLastLocation(history.location.state)
      ) {
        console.log('REPLACE ROUTE');
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
    [router.actionTypes.locationChanged]: () => {
      console.log('LOCATION CHANGED');
    },
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
  selectors({
    searchParams: [
      () => [router.selectors.searchParams],
      (searchParams) => searchParams as Record<string, unknown>,
    ],
    hashParams: [
      () => [router.selectors.hashParams],
      (hashParams) => {
        console.log('ROUTE LOGIC');
        console.log(hashParams);
        return hashParams as Record<string, unknown>;
      },
    ],
  }),
  afterMount(() => {
    history.listen((update) => {
      console.log(update);
      if (
        update.location.pathname != router.values.location.pathname ||
        update.location.search != router.values.location.search ||
        update.location.hash != router.values.location.hash
      ) {
        console.log(decodeParams(update.location.hash, '#'));
        router.actions.locationChanged({
          method: update.action,
          ...update.location,
          url: update.location.pathname,
          hashParams: decodeParams(update.location.hash, '#'),
          searchParams: decodeParams(update.location.search, '?'),
        });
      }
    });
  }),
]);

export const routeLogic = injectDepsToLogic(logic, () => ({
  routeValidators: Dependencies.get(IRouteValidators.$),
}));
