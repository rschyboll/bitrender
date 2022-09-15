import { enableMapSet } from 'immer';
import { resetContext } from 'kea';
import { localStoragePlugin } from 'kea-localstorage';
import { routerPlugin } from 'kea-router';
import { subscriptionsPlugin } from 'kea-subscriptions';

import Dependencies from '@/deps';
import { ISettingsLogic } from '@/logic/interfaces';
import { history } from '@/pages/router';

import { IRouteLogic } from './interfaces/route';

export const startKea = () => {
  enableMapSet();
  resetContext({
    plugins: [
      subscriptionsPlugin,
      localStoragePlugin,
      routerPlugin({
        location: history.location as unknown as undefined,
        history: {
          replaceState: (
            state: Record<string, unknown>,
            _: string,
            url: string,
          ) => {
            //Workaround, without this, kea changes routes when components in react are still rendering
            //which can cause a logic from kea to not unmount properly
            console.log(state);
            setTimeout(() => {
              history.replace(url, state);
            }, 0);
          },
          pushState: (
            state: Record<string, unknown>,
            _: string,
            url: string,
          ) => {
            console.log(state);

            setTimeout(() => {
              history.push(url, state);
            }, 0);
          },
        } as unknown as undefined,
      }),
    ],
  });
};

export const startGlobalLogics = () => {
  Dependencies.get(ISettingsLogic.$).mount();
  Dependencies.get(IRouteLogic.$).mount();
};
