import type { interfaces } from 'inversify';
import type { LogicWrapper } from 'kea';

import type { MakeOwnLogicType } from '@/logic/types/makeLogic';
import type { MRole } from '@/types/models';

interface Actions {
  addEntries: (entries: MRole.View[]) => {
    entries: MRole.View[];
  };
  useEntries: (entryIds: string[] | Set<string>) => { entryIds: string[] };
  releaseEntries: (entryIds: string[] | Set<string>) => { entryIds: string[] };
  forceCleanup: true;
}

interface Values {
  entries: Map<string, MRole.View>;
}

export type IRoleUserCountContainerLogic = LogicWrapper<
  MakeOwnLogicType<{
    actions: Actions;
    values: Values;
  }>
>;

export namespace IRoleUserCountContainerLogic {
  export const $: interfaces.ServiceIdentifier<IRoleUserCountContainerLogic> =
    Symbol('IRoleUserCountContainerLogic');
}
