import { actions, kea, listeners, props, reducers } from 'kea';

import Dependencies from '@/deps';
import { injectDepsToLogic } from '@/logic/utils';
import { IUserService } from '@/services/interfaces';

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
    logout: true,
  }),
  reducers({
    loginLoading: [false],
    loginSuccess: [false],
    loginFailure: [false],
    logoutLoading: [false],
    logoutSuccess: [false],
    logoutFailure: [false],
  }),
  listeners(({}) => ({
    login: async () => {},
  })),
]);

export const loginLogic = injectDepsToLogic(logic, () => ({
  userService: Dependencies.get(IUserService.$),
}));
