import { actions, afterMount } from 'kea';
import { listeners } from 'kea';
import { kea, key, path, reducers } from 'kea';

import { sleep } from '@/utils/async';

import { Reducers } from './reducers';
import type { SettingsLogicType } from './type';

const logic = kea<SettingsLogicType>([
  path(['test', 'single']),
  key((props) => props.key),
  actions({
    updateValue: true,
  }),
  reducers(Reducers),
  listeners(({ actions }) => ({
    updateValue: async () => {
      await sleep(1000);
      actions.updateValue();
    },
  })),
  afterMount(({ actions }) => {
    actions.updateValue();
  }),
]);

export const testSingleLogic = logic;
