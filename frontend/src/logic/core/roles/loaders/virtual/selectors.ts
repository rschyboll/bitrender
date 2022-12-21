import type { SelectorsDef } from '@/logic/types';
import type { MRole } from '@/types/models';

import type { RoleVirtualLoaderLogic } from './type';

export const Selectors: SelectorsDef<RoleVirtualLoaderLogic> = ({ deps }) => ({
  entries: [
    (selectors) => [
      deps.roleViewContainerLogic.selectors.entries,
      selectors.loadedEntryIds,
      selectors.entryCount,
    ],
    (entries, loadedEntryIds, entryCount) => {
      if (entryCount == null) {
        return Array.from({ length: 100 });
      }
      const tableViews: MRole.View[] = Array.from({ length: entryCount });

      loadedEntryIds.forEach((loadedEntryId, loadedEntryIndex) => {
        const entry = entries.get(loadedEntryId);
        if (entry != null) {
          tableViews[loadedEntryIndex] = entry;
        }
      });

      return tableViews;
    },
  ],
});
