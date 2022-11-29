import type { ListenersDef } from '@/logic/types';

import type { RoleViewContainerLogic } from './type';

export const Listeners: ListenersDef<RoleViewContainerLogic> = ({
  actions,
  values,
}) => ({
  startGarbageCollection: async (_, breakpoint) => {
    while (values.garbageCollectionRunning) {
      const currentTime = new Date().getTime();
      const entryIdsToRemove: string[] = [];
      values.usageCounters.forEach((usageCounter, id) => {
        if (
          usageCounter.counter <= 0 &&
          currentTime - usageCounter.lastUseTime.getTime() >= 5000
        ) {
          entryIdsToRemove.push(id);
        }
      });
      if (entryIdsToRemove.length > 0) {
        actions.removeEntries(entryIdsToRemove);
      }
      await breakpoint(5000);
    }
  },
  forceCleanup: () => {
    const entryIdsToRemove: string[] = [];
    values.usageCounters.forEach((usageCounter, id) => {
      entryIdsToRemove.push(id);
    });
    if (entryIdsToRemove.length > 0) {
      actions.removeEntries(entryIdsToRemove);
    }
  },
});
