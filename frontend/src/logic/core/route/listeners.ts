import { Path } from 'history';

import type { ListenersDef, SharedListenersDef } from '@/logic/types';
import { history } from '@/pages/router';

import type { RouteLogicType } from './type';

export const SharedListeners: SharedListenersDef<RouteLogicType> = ({
  deps,
}) => ({
  pushRoute: (payload: { to: string | Partial<Path>; state?: object }) => {
    history.push(payload.to, {
      ...payload.state,
      lastLocation: { ...history.location },
    });
  },
  replaceRoute: (payload: { to: string | Partial<Path>; state?: object }) => {
    if (deps.routeValidators.stateHasLastLocation(history.location.state)) {
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
    if (deps.routeValidators.stateHasLastLocation(history.location.state)) {
      history.replace(
        history.location.state.lastLocation.pathname,
        history.location.state.lastLocation.state,
      );
    } else {
      history.replace('/app');
    }
  },
});

export const Listeners: ListenersDef<RouteLogicType> = ({
  sharedListeners,
}) => ({
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
});
