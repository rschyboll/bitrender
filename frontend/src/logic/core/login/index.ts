import { actions, kea, listeners, path, props, reducers } from 'kea';

import Dependencies from '@/deps';
import { IRouteLogic } from '@/logic/interfaces/route';
import { injectDepsToLogic } from '@/logic/utils';
import { IUserService } from '@/services/interfaces';
import { RequestStatus } from '@/types/service';
import { sleep } from '@/utils/async';
import { IUserValidators } from '@/validators/interfaces';

import type { logicType } from './indexType';

const logic = kea<logicType>([
  path(['login']),
  props(
    {} as {
      deps: {
        routeLogic: IRouteLogic;
        userService: IUserService;
        userValidators: IUserValidators;
      };
    },
  ),
  actions({
    checkLoggedIn: true,
    login: (username: string, password: string) => ({ username, password }),
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
      RequestStatus.Idle as RequestStatus,
      {
        login: () => RequestStatus.Loading,
        loginSuccess: () => RequestStatus.Success,
        loginFailure: () => RequestStatus.Error,
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
      RequestStatus.Idle as RequestStatus,
      {
        logout: () => RequestStatus.Loading,
        logoutSuccess: () => RequestStatus.Success,
        logoutFailure: () => RequestStatus.Error,
      },
    ],
    registerStatus: [
      RequestStatus.Idle as RequestStatus,
      {
        register: () => RequestStatus.Loading,
        registerSuccess: () => RequestStatus.Success,
        registerFailure: () => RequestStatus.Error,
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
  listeners(({ props, actions, values }) => ({
    checkLoggedIn: async () => {
      const response = await props.deps.userService.logged();
      if (response.success && response.data) {
        props.deps.routeLogic.actions.openApp();
      } else if (!response.success) {
        await sleep(250);
        actions.checkLoggedIn();
      }
    },
    login: async ({ username, password }) => {
      const response = await props.deps.userService.login(username, password);
      if (response.success) {
        actions.loginSuccess();
      } else {
        if ('detail' in response.error) {
          actions.loginFailure(response.error.detail);
        } else {
          actions.loginFailure();
        }
      }
    },
    loginSuccess: () => {
      props.deps.routeLogic.actions.returnToBeforeLogin();
    },
    register: async ({ email, username, password }) => {
      if (!props.deps.userValidators.validateUserPasswordStrength(password)) {
        actions.setRegisterWeakPassword(true);
        actions.registerResetStatus();
        return;
      } else if (values.registerWeakPassword) {
        actions.setRegisterWeakPassword(false);
      }

      if (!props.deps.userValidators.validateUserEmail(email)) {
        actions.setRegisterWrongEmail(true);
        actions.registerResetStatus();
        return;
      } else if (values.registerWrongEmail) {
        actions.setRegisterWrongEmail(false);
      }

      const response = await props.deps.userService.register({
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
  })),
]);

export const loginLogic = injectDepsToLogic(logic, () => ({
  routeLogic: Dependencies.get(IRouteLogic.$),
  userService: Dependencies.get(IUserService.$),
  userValidators: Dependencies.get(IUserValidators.$),
}));
