import { enableMapSet } from 'immer';
import { resetContext } from 'kea';
import { localStoragePlugin } from 'kea-localstorage';
import { routerPlugin } from 'kea-router';

import Dependencies from '@/deps';
import { IAppLogic, ISettingsLogic } from '@/logic/interfaces';

export const startKea = () => {
  enableMapSet();
  resetContext({
    plugins: [localStoragePlugin, routerPlugin({})],
  });
};

export const startGlobalLogics = () => {
  Dependencies.get(ISettingsLogic.$).mount();
  Dependencies.get(IAppLogic.$).mount();
};
