import produce from 'immer';

import type { ReducersDef } from '@/logic';

import type { CreateRoleLogic } from './type';

export const Reducers: ReducersDef<CreateRoleLogic> = {
  selectedPermissions: [
    new Set(),
    {
      setPermissionSelected: (immutableState, { permission, checked }) =>
        produce(immutableState, (state) => {
          console.log(checked);
          if (checked) {
            state.add(permission);
          } else {
            state.delete(permission);
          }
        }),
    },
  ],
  name: [
    '',
    {
      setName: (_, { name }) => name,
    },
  ],
  isDefault: [null, { setDefault: (_, { isDefault }) => isDefault }],
};
