import { actions, afterMount, kea, listeners, props, reducers } from 'kea';
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
  actionToUrl(() => ({
    openApp: () => `/app`,
  })),
  actions({
    loadCurrentUser: true,
    openApp: true,
  }),
  reducers({}),
  listeners(({ props }) => ({
    loadCurrentUser: async () => {
      const me = await props.deps.userService.getCurrentUser();
      console.log(me);
    },
  })),
  afterMount(({ actions }) => {
    actions.loadCurrentUser();
  }),
]);

export const appLogic = injectDepsToLogic(logic, () => ({
  userService: Dependencies.get(IUserService.$),
}));
