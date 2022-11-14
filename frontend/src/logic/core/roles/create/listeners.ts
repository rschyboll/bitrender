import type { ListenersDef } from '@/logic/types';

import type { CreateRoleLogic } from './type';

export const Listeners: ListenersDef<CreateRoleLogic> = ({
  actions,
  values,
}) => ({
  save: () => {
    actions.create({
      name: values.name,
      default: values.isDefault,
      permissions: Array.from(values.selectedPermissions),
    });
  },
});
