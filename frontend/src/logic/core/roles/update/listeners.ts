import type { ListenersDef } from '@/logic/types';

import type { RoleUpdateLogic } from './type';

export const Listeners: ListenersDef<RoleUpdateLogic> = ({
  actions,
  values,
}) => ({
  save: () => {
    if (values.name.length < 4) {
      return;
    }
    actions.create({
      name: values.name,
      default: values.isDefault,
      permissions: Array.from(values.selectedPermissions),
    });
  },
});
