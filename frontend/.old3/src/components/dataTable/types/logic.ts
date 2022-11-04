import { LogicWrapper } from 'kea';

import { MakeOwnLogicType } from '@/logic/types/makeLogic';

interface Actions {
  setCurrentPage: (currentPage: number) => void;
  setRowsPerPage: (rowsPerPage: number) => void;
}

interface Values {
  currentPage: number;
  rowsPerPage: number;
  amountOfRecords: number | null;
  values: Record<string, unknown>[];
}

export type IDataTableLogic = LogicWrapper<
  MakeOwnLogicType<{
    values: Values;
    actions: Actions;
  }>
>;
