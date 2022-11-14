import { deepEqual } from 'fast-equals';
import { Path } from 'history';
import { Location } from 'history';
import {
  actions,
  afterMount,
  kea,
  listeners,
  path,
  reducers,
  selectors,
  sharedListeners,
} from 'kea';

import { deps } from '@/logic/builders';
import { history } from '@/pages/router';
import { IRouteValidators } from '@/validators/interfaces';

import { Listeners, SharedListeners } from './listeners';
import { Reducers } from './reducers';
import { Selectors } from './selectors';
import type { RouteLogicType } from './type';

export const routeLogic = kea<RouteLogicType>([
  path(['route']),
  deps({
    routeValidators: IRouteValidators.$,
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
  reducers(Reducers),
  selectors(Selectors),
  sharedListeners(SharedListeners),
  listeners(Listeners),
  afterMount(({ actions, values }) => {
    history.listen((update) => {
      if (!deepEqual(update.location, values.currentLocation)) {
        actions.updateLocationState(update.location);
      }
    });
  }),
]);
