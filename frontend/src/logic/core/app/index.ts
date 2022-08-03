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
import { IUserService } from '@/services/interfaces';
import { UserView } from '@/types/user';
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
      console.log('LOAD CURRENT USER');
      const response = await props.deps.userService.getCurrentUser();
      console.log(response);
      if (response.success) {
        console.log(response.data);
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
    console.log('APP LOGIC MOUNTED');
    actions.loadCurrentUser();
  }),
  beforeUnmount(() => {
    console.log('APP LOGIC UNMOUNTED');
  }),
]);

export const appLogic = injectDepsToLogic(logic, () => ({
  userService: Dependencies.get(IUserService.$),
}));
