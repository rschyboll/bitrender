import type { SelectorsDef } from '@/logic/types';
import type { MRole } from '@/types/models';

import type { RoleTableLoaderLogic } from './type';

export const Selectors: SelectorsDef<RoleTableLoaderLogic> = ({ deps }) => ({
  entries: [
    (selectors) => [
      deps.roleViewContainerLogic.selectors.entries,
      selectors.loadedEntryIds,
    ],
    (entries, loadedEntryIds) => {
      const tableViews: MRole.TableView[] = [];

      loadedEntryIds.forEach((id) => {
        const roleView = entries.get(id);
        if (roleView != null) {
          tableViews.push(deps.roleConverters.viewToTableView(roleView));
        }
      });

      return tableViews;
    },
  ],
});
