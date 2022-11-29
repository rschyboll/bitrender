import type { ReducersDef } from '@/logic';

import type { RolesTableLogic } from './type';

export const Reducers: ReducersDef<RolesTableLogic> = {
  localSearchString: [
    null,
    {
      setSearchString: (_, { searchString }) => searchString,
    },
  ],
};
