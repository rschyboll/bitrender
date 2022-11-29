import type { MakeOwnLogicType } from '@/logic';
import type { MRole } from '@/types/models';

interface Actions {
  startGarbageCollection: true;
  stopGarbageCollection: true;
  addEntries: (entries: MRole.View[]) => {
    entries: MRole.View[];
  };
  removeEntries: (entryIds: string[]) => { entryIds: string[] };
  useEntries: (entryIds: string[]) => { entryIds: string[] };
  releaseEntries: (entryIds: string[]) => { entryIds: string[] };
  forceCleanup: true;
}

interface Reducers {
  entries: Map<string, MRole.View>;
  usageCounters: Map<string, { counter: number; lastUseTime: Date }>;
  garbageCollectionRunning: boolean;
}

export type RoleViewContainerLogic = MakeOwnLogicType<{
  actions: Actions;
  reducers: Reducers;
}>;
