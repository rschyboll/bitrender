import produce from 'immer';

import type { ReducersDef } from '@/logic';

import type { RoleVirtualLoaderLogic } from './type';

export const Reducers: ReducersDef<RoleVirtualLoaderLogic> = {
  loadedEntryIds: [
    new Map(),
    {
      addLoadedEntryIds: (immutableState, { entryIds, offset }) =>
        produce(immutableState, (state) => {
          let index = 0;
          entryIds.forEach((entryId) => {
            state.set(index + offset, entryId);
            index++;
          });
        }),
    },
  ],
  entryCount: [
    null,
    {
      setEntryRowCount: (_, { rowCount }) => rowCount,
    },
  ],
};
