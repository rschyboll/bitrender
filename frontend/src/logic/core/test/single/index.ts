import { kea, key, path, reducers } from 'kea';

import { Reducers } from './reducers';
import type { SettingsLogicType } from './type';

const logic = kea<SettingsLogicType>([
  path(['test', 'single']),
  key((props) => props.key),
  reducers(Reducers),
]);

export const testSingleLogic = logic;
