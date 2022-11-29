import type { ReducersDef } from '@/logic';

import type { RoleTableLoaderLogic } from './type';

export const Reducers: ReducersDef<RoleTableLoaderLogic> = {
  loadedEntryIds: [
    [],
    {
      setLoadedEntryIds: (_, { entryIds }) => entryIds,
    },
  ],
  entryCount: [
    0,
    {
      setEntryRowCount: (_, { rowCount }) => rowCount,
    },
  ],
};
