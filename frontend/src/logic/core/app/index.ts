import { afterMount, kea, listeners, path, reducers } from 'kea';

import { deps } from '@/logic/builders';
import { requests } from '@/logic/builders/requests';
import { UserView } from '@/schemas/user';
import { IUserService } from '@/services/interfaces';
import { sleep } from '@/utils/async';

import type { AppLogicType } from './type';

export const appLogic = kea<AppLogicType>([
  path(['app']),
  deps({
    userService: IUserService.$,
  }),
  requests(({ deps }) => ({
    loadCurrentUser: deps.userService.getCurrentUser,
  })),
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
        loadCurrentUserSuccess: (_, currentUser) => currentUser,
      },
    ],
  }),
  listeners(({ actions }) => ({
    loadCurrentUserFailure: async () => {
      await sleep(2000);
      actions.loadCurrentUser();
    },
  })),
  afterMount(({ actions }) => {
    actions.loadCurrentUser();
  }),
]);
