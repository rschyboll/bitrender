import { afterMount, beforeUnmount } from 'kea';
import { actions, kea, listeners, path, reducers } from 'kea';

import { Listeners } from './listeners';
import { Reducers } from './reducers';
import type { RoleViewContainerLogic } from './type';

export const roleViewContainerLogic = kea<RoleViewContainerLogic>([
  path(['roles', 'container', 'view']),
  actions({
    startGarbageCollection: true,
    stopGarbageCollection: true,
    addEntries: (entries) => ({ entries }),
    removeEntries: (entryIds) => ({ entryIds }),
    useEntries: (entryIds) => ({ entryIds }),
    releaseEntries: (entryIds) => ({ entryIds }),
    forceCleanup: true,
  }),
  reducers(Reducers),
  listeners(Listeners),
  afterMount(({ actions }) => {
    actions.startGarbageCollection();
  }),
  beforeUnmount(({ actions }) => {
    actions.stopGarbageCollection();
  }),
]);
