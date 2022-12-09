import produce from 'immer';

import type { ReducersDef } from '@/logic';

import type { RoleCreateLogic } from './type';

export const Reducers: ReducersDef<RoleCreateLogic> = {
  selectedPermissions: [
    new Set(),
    {
      setPermissionSelected: (immutableState, { permission, checked }) =>
        produce(immutableState, (state) => {
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
  saveClicked: [false, { save: () => true }],
};
