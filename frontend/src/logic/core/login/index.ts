import { actions, kea, listeners, props, reducers } from 'kea';

import Dependencies from '@/deps';
import { IRouteLogic } from '@/logic/interfaces/route';
import { injectDepsToLogic } from '@/logic/utils';
import { IUserService } from '@/services/interfaces';
import { RequestStatus } from '@/types/service';

import type { logicType } from './indexType';

const logic = kea<logicType>([
  props(
    {} as {
      deps: {
        routeLogic: IRouteLogic;
        userService: IUserService;
      };
    },
  ),
  actions({
    login: (username: string, password: string) => ({ username, password }),
    loginSuccess: true,
    loginFailure: (errorDetail?: unknown) => ({ errorDetail }),
    logout: true,
    logoutSuccess: true,
    logoutFailure: (errorDetail?: unknown) => ({ errorDetail }),
    register: (username: string, password: string) => ({ username, password }),
    registerSuccess: true,
    registerFailure: true,
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
      },
    ],
  }),
  listeners(({ props, actions }) => ({
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
  })),
]);

export const loginLogic = injectDepsToLogic(logic, () => ({
  routeLogic: Dependencies.get(IRouteLogic.$),
  userService: Dependencies.get(IUserService.$),
}));
