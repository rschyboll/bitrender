import { actions, afterMount, kea, listeners, props, reducers } from 'kea';

import Dependencies from '@/deps';
import { injectDepsToLogic } from '@/logic/utils';
import { IUserService } from '@/services/interfaces';
import { UserView } from '@/types/user';
import { sleep } from '@/utils/async';

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
    loadCurrentUserSuccess: (currentUser: UserView) => ({ currentUser }),
    loadCurrentUserFailure: true,
  }),
  reducers({
    appReady: [
      false,
      {
        loadCurrentUserSuccess: () => true,
      },
    ],
    currentUser: [
      null as UserView | null,
      {
        loadCurrentUserSuccess: (_, { currentUser }) => currentUser,
      },
    ],
  }),
  listeners(({ props, actions }) => ({
    loadCurrentUser: async () => {
      const response = await props.deps.userService.getCurrentUser();
      if (response.success) {
        actions.loadCurrentUserSuccess(response.data);
      } else {
        actions.loadCurrentUserFailure();
      }
    },
    loadCurrentUserFailure: async () => {
      await sleep(2000);
      actions.loadCurrentUser();
    },
  })),
  afterMount(({ actions }) => {
    actions.loadCurrentUser();
    console.log('TESTTTTTT');
  }),
]);

export const appLogic = injectDepsToLogic(logic, () => ({
  userService: Dependencies.get(IUserService.$),
}));
