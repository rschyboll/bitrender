import type { ReducersDef } from '@/logic';

import type { RoleTableLoaderLogic } from './type';

export const Reducers: ReducersDef<RoleTableLoaderLogic> = {
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
