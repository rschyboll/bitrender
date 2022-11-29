import type { ListenersDef } from '@/logic/types';

import type { RoleTableLoaderLogic } from './type';

export const Listeners: ListenersDef<RoleTableLoaderLogic> = ({ actions }) => ({
  loadSuccess: async ({ value }) => {
    actions.setEntryRowCount(value.rowCount);
    actions.setLoadedEntryIds(
      value.items.map((roleView) => {
        return roleView.id;
      }),
    );
  },
});
