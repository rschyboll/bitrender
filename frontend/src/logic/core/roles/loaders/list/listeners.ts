import type { ListenersDef } from '@/logic/types';

import type { RoleListLoaderLogic } from './type';

export const Listeners: ListenersDef<RoleListLoaderLogic> = ({
  actions,
  values,
  deps,
}) => ({
  loadSuccess: async ({ value }) => {
    deps.roleViewContainerLogic.actions.releaseEntries(values.loadedEntryIds);
    const entryIds = value.items.map((roleView) => {
      return roleView.id;
    });

    actions.setEntryRowCount(value.rowCount);
    actions.setLoadedEntryIds(entryIds);
    deps.roleViewContainerLogic.actions.addEntries(value.items);
    deps.roleViewContainerLogic.actions.useEntries(entryIds);
  },
});
