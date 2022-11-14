import { actions, kea, listeners, path, reducers } from 'kea';
import { urlToAction } from 'kea-router';

import { deps } from '@/logic/builders';
import { IRouteLogic } from '@/logic/interfaces';
import { IUserService } from '@/services/interfaces';
import { IUserValidators } from '@/validators/interfaces';

import { Listeners } from './listeners';
import { Reducers } from './reducers';
import type { AuthLogic } from './type';

export const authLogic = kea<AuthLogic>([
  path(['auth']),
  deps({
    routeLogic: IRouteLogic.$,
    userService: IUserService.$,
    userValidators: IUserValidators.$,
  }),
  urlToAction(({ actions }) => ({
    '/login': () => actions.checkLoggedIn(),
    '/register': () => actions.checkLoggedIn(),
    '/verify': () => actions.checkLoggedIn(),
  })),
  actions({
    checkLoggedIn: true,
    login: (username: string, password: string) => ({
      username: username,
      password,
    }),
    loginSuccess: true,
    loginFailure: (errorDetail?: unknown) => ({ errorDetail }),
    logout: true,
    logoutSuccess: true,
    logoutFailure: (errorDetail?: unknown) => ({ errorDetail }),
    register: (email: string, username: string, password: string) => ({
      email,
      username,
      password,
    }),
    registerSuccess: true,
    registerFailure: (errorDetail?: unknown) => ({ errorDetail }),
    registerResetStatus: true,
    setRegisterWeakPassword: (weakPassword: boolean) => ({ weakPassword }),
    setRegisterWrongEmail: (wrongEmail: boolean) => ({ wrongEmail }),
  }),
  reducers(Reducers),
  listeners(Listeners),
]);
