import { actions, kea, listeners, props, reducers } from 'kea';
import { actionToUrl } from 'kea-router';

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
    loadCurrentUser: true,
  }),
  reducers({}),
  listeners(({ props }) => ({
    loadCurrentUser: async () => {
      const me = await props.deps.userService.getMe();
    },
  })),
]);

export const appLogic = injectDepsToLogic(logic, () => ({
  userService: Dependencies.get(IUserService.$),
}));
