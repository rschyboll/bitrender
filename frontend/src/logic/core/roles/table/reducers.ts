/* eslint-disable @typescript-eslint/no-dynamic-delete */
import type { ReducersDef } from '@/logic';
import { RequestStatus } from '@/services';

import type { RolesTableLogic } from './type';

export const Reducers: ReducersDef<RolesTableLogic> = {
  localSearchString: [
    null,
    {
      setSearchString: (_, { searchString }) => searchString,
    },
  ],
  loadState: [
    RequestStatus.Idle,
    {
      load: () => RequestStatus.Running,
      loadSuccess: () => RequestStatus.Success,
      loadFailure: () => RequestStatus.Failure,
    },
  ],
  roles: [
    [],
    {
      loadSuccess: (_, { roles }) => roles,
    },
  ],
  amountOfRecords: [
    0,
    {
      loadSuccess: (_, { rowCount }) => rowCount,
    },
  ],
};