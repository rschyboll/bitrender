import type { interfaces } from 'inversify';
import type { LogicWrapper } from 'kea';

import type { MakeOwnLogicType } from '@/logic/types/makeLogic';
import type { MRole } from '@/types/models';

interface Actions {
  addEntries: (
    entries:
      | Map<string, MRole.View>
      | Record<string, MRole.View>
      | MRole.View[],
  ) => {
    entries:
      | Map<string, MRole.View>
      | Record<string, MRole.View>
      | MRole.View[];
  };
  useEntries: (entryIds: string[] | Set<string>) => { entryIds: string[] };
  releaseEntries: (entryIds: string[] | Set<string>) => { entryIds: string[] };
  forceCleanup: true;
}

interface Values {
  entries: Map<string, MRole.View>;
}

export type IRoleViewContainerLogic = LogicWrapper<
  MakeOwnLogicType<{
    actions: Actions;
    values: Values;
  }>
>;

export namespace IRoleViewContainerLogic {
  export const $: interfaces.ServiceIdentifier<IRoleViewContainerLogic> =
    Symbol('IRoleViewContainerLogic');
}
