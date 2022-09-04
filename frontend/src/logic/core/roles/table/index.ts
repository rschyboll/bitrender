import { actions, kea, listeners, path, reducers } from 'kea';

import { injectDepsToLogic } from '@/logic/utils';

import type { logicType } from './indexType';

const logic = kea<logicType>([
  path(['roles', 'table']),
  actions({
    setCurrentPage: (currentPage: number) => ({ currentPage }),
    setRowsPerPage: (rowsPerPage: number) => ({ rowsPerPage }),
  }),
  reducers({
    currentPage: [0],
    rowsPerPage: [10],
    amountOfRecords: [null as number | null],
  }),
  listeners(({ props, actions, values }) => ({})),
]);

export const rolesTableLogic = injectDepsToLogic(logic, () => ({}));
