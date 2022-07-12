import { kea, reducers } from 'kea';
import { actionToUrl } from 'kea-router';

import type { logicType } from './indexType';

const logic = kea<logicType>([
  reducers({}),
  actionToUrl(({}) => ({
    openTask: ({ id }) => `/articles/${id}`,
  })),
]);

export const appLogic = logic;
