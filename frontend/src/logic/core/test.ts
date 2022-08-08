import { kea, path } from 'kea';

import type { logicType } from './testType';

const logic = kea<logicType>([path(['test'])]);

export const testLogic = logic;
