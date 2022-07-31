import { actions, kea, listeners, props, reducers } from 'kea';

import Dependencies from '@/deps';
import { injectDepsToLogic } from '@/logic/utils';
import { IUserService } from '@/services/interfaces';
import { RequestStatus } from '@/types/service';

import type { logicType } from './indexType';

const logic = kea<logicType>([
  props(
    {} as {
      deps: {
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
  })),
]);

export const loginLogic = injectDepsToLogic(logic, () => ({
  userService: Dependencies.get(IUserService.$),
}));
