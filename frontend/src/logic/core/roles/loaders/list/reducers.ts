import type { ReducersDef } from '@/logic';

import type { RoleListLoaderLogic } from './type';

export const Reducers: ReducersDef<RoleListLoaderLogic> = {
  loadedEntryIds: [
    new Set(),
    {
      setLoadedEntryIds: (_, { entryIds }) =>
        entryIds instanceof Set ? entryIds : new Set(entryIds),
    },
  ],
  entryCount: [
    0,
    {
      setEntryRowCount: (_, { rowCount }) => rowCount,
    },
  ],
};
