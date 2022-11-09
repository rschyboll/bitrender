import type { Location, Path } from 'history';

import type { MakeOwnLogicType } from '@/logic/types';
import { IRouteValidators } from '@/validators/interfaces';

interface Reducers {
  currentLocation: Location;
}

interface Actions {
  updateLocationState: (location: Location) => { location: Location };
  openRoute: (
    to: string | Partial<Path>,
    state?: object,
  ) => { to: string | Partial<Path>; state?: object };
  replaceRoute: (
    to: string | Partial<Path>,
    state?: object,
  ) => { to: string | Partial<Path>; state?: object };
  openApp: () => { to: string };
  openRegisterPage: () => { to: string };
  openLoginPage: () => { to: string };
  openVerifyPage: (email: string) => {
    to: string;
    state: { verifyEmail: string };
  };
  openUsersPage: () => { to: string };
  openRolesPage: (
    page: number,
    rows: number,
    search: null | string,
  ) => { to: string };
}

interface Selectors {
  pathname: (currentLocation: Location) => string;
  search: (currentLocation: Location) => string;
  hash: (currentLocation: Location) => string;
  state: (currentLocation: Location) => unknown;
  key: (currentLocation: Location) => string;
  searchParams: (search: string) => Record<string, unknown>;
  hashParams: (hash: string) => Record<string, unknown>;
}

interface SharedListeners {
  pushRoute: () => Promise<void>;
}

interface Deps {
  routeValidators: IRouteValidators;
}

export type RouteLogicType = MakeOwnLogicType<{
  reducers: Reducers;
  selectors: Selectors;
  sharedListeners: SharedListeners;
  deps: Deps;
}>;
