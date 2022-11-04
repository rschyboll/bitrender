import {
  actions,
  afterMount,
  beforeUnmount,
  kea,
  listeners,
  path,
  props,
  reducers,
} from 'kea';

import Dependencies from '@/deps';
import { injectDepsToLogic } from '@/logic/utils';
import { UserView } from '@/schemas/user';
import { IUserService } from '@/services/interfaces';
import { sleep } from '@/utils/async';

import type { logicType } from './indexType';

const logic = kea<logicType>([
  path(['app']),
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
  }),
  beforeUnmount(() => {}),
]);

export const appLogic = injectDepsToLogic(logic, () => ({
  userService: Dependencies.get(IUserService.$),
}));
