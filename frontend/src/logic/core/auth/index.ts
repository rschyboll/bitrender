import { actions, kea, listeners, path, reducers } from 'kea';
import { urlToAction } from 'kea-router';

import { deps } from '@/logic/builders';
import { IRouteLogic } from '@/logic/interfaces';
import {
  ApiErrorCodes,
  RequestStatus,
  ServiceErrorType,
} from '@/services/enums';
import { IUserService } from '@/services/interfaces';
import { sleep } from '@/utils/async';
import { IUserValidators } from '@/validators/interfaces';

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
  reducers({
    loginStatus: [
      RequestStatus.Idle,
      {
        login: () => RequestStatus.Idle,
        loginSuccess: () => RequestStatus.Success,
        loginFailure: () => RequestStatus.Failure,
      },
    ],
    loginErrorDetail: [
      null as null | unknown,
      {
        loginFailure: (_, { errorDetail }) =>
          errorDetail !== undefined ? errorDetail : null,
      },
    ],
    logoutStatus: [
      RequestStatus.Idle,
      {
        logout: () => RequestStatus.Idle,
        logoutSuccess: () => RequestStatus.Success,
        logoutFailure: () => RequestStatus.Failure,
      },
    ],
    registerStatus: [
      RequestStatus.Idle as RequestStatus,
      {
        register: () => RequestStatus.Idle,
        registerSuccess: () => RequestStatus.Success,
        registerFailure: () => RequestStatus.Failure,
        registerResetStatus: () => RequestStatus.Idle,
      },
    ],
    registerWeakPassword: [
      false,
      {
        setRegisterWeakPassword: (_, { weakPassword }) => weakPassword,
      },
    ],
    registerWrongEmail: [
      false,
      {
        setRegisterWrongEmail: (_, { wrongEmail }) => wrongEmail,
      },
    ],
    registerErrorDetail: [
      null as null | unknown,
      {
        registerFailure: (_, { errorDetail }) =>
          errorDetail !== undefined ? errorDetail : null,
      },
    ],
  }),
  listeners(({ actions, values, deps }) => ({
    checkLoggedIn: async () => {
      const response = await deps.userService.logged();
      if (response.success && response.data) {
        deps.routeLogic.actions.openApp();
      } else if (!response.success) {
        await sleep(1000);
        actions.checkLoggedIn();
      }
    },
    login: async ({ username, password }) => {
      const response = await deps.userService.login(username, password);
      if (response.success) {
        actions.loginSuccess();
      } else {
        if ('detail' in response.error) {
          if (response.error.detail == ApiErrorCodes.UserNotVerified) {
            deps.routeLogic.actions.openVerifyPage(username);
          }
          actions.loginFailure(response.error.detail);
        } else {
          actions.loginFailure();
        }
      }
    },
    loginSuccess: () => {
      deps.routeLogic.actions.returnToBeforeLogin();
    },
    register: async ({ email, username, password }) => {
      if (!deps.userValidators.validateUserPasswordStrength(password)) {
        actions.setRegisterWeakPassword(true);
        actions.registerResetStatus();
        return;
      } else if (values.registerWeakPassword) {
        actions.setRegisterWeakPassword(false);
      }

      if (!deps.userValidators.validateUserEmail(email)) {
        actions.setRegisterWrongEmail(true);
        actions.registerResetStatus();
        return;
      } else if (values.registerWrongEmail) {
        actions.setRegisterWrongEmail(false);
      }

      const response = await deps.userService.register({
        email,
        username,
        password,
      });
      if (response.success) {
        actions.registerSuccess();
      } else {
        if ('detail' in response.error) {
          actions.registerFailure(response.error.detail);
        } else {
          actions.registerFailure();
        }
      }
    },
    logout: async () => {
      const response = await deps.userService.logout();
      if (response.success) {
        deps.routeLogic.actions.openLoginPage();
      } else {
        if (
          response.error.type == ServiceErrorType.ApiError &&
          response.error.detail == ApiErrorCodes.NotAuthenticated
        ) {
          deps.routeLogic.actions.openLoginPage();
        }
      }
    },
  })),
]);
