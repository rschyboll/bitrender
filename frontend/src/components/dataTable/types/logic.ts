import { LogicWrapper, MakeLogicType } from 'kea';

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

export type IDataTableLogic = LogicWrapper<MakeLogicType<Values, Actions>>;
