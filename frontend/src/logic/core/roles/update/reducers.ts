import type { ReducersDef } from '@/logic';
import { MRole } from '@/types/models';

import type { RoleUpdateLogic } from './type';

export const Reducers: ReducersDef<RoleUpdateLogic> = ({ deps }) => ({
  selectedPermissions: [
    deps.roleViewLoaderLogic.values.entry != null
      ? new Set(deps.roleViewLoaderLogic.values.entry.permissions)
      : new Set<MRole.Permission>(),
  ],
  name: [
    deps.roleViewLoaderLogic.values.entry != null
      ? deps.roleViewLoaderLogic.values.entry.name
      : '',
  ],
  isDefault: [
    deps.roleViewLoaderLogic.values.entry != null
      ? deps.roleViewLoaderLogic.values.entry.default
      : null,
  ],
  saveClicked: [false],
});
