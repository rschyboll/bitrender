import { enableMapSet } from 'immer';
import { resetContext } from 'kea';
import { localStoragePlugin } from 'kea-localstorage';
import { routerPlugin } from 'kea-router';

import Dependencies from '@/deps';
import { IAppLogic, ISettingsLogic } from '@/logic/interfaces';
import { history } from '@/pages/history';

export const startKea = () => {
  enableMapSet();
  resetContext({
    plugins: [
      localStoragePlugin,
      routerPlugin({
        location: history.location as unknown as undefined,
        history: {
          replaceState: (
            state: Record<string, unknown>,
            _: string,
            url: string,
          ) => {
            history.replace(url, state);
          },
          pushState: (
            state: Record<string, unknown>,
            _: string,
            url: string,
          ) => {
            history.push(url, state);
          },
        } as unknown as undefined,
      }),
    ],
  });
};

export const startGlobalLogics = () => {
  Dependencies.get(ISettingsLogic.$).mount();
  Dependencies.get(IAppLogic.$).mount();
};
