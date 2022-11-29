import type { interfaces } from 'inversify';
import type { LogicWrapper } from 'kea';

import type { MakeOwnLogicType } from '@/logic/types/makeLogic';
import type { RequestStatus } from '@/services';
import type { MRole } from '@/types/models';

interface Actions {
  load: (input: MRole.Messages.GetListInput) => {
    input: MRole.Messages.GetListInput;
  };
}

interface Values {
  entries: MRole.TableView[];
  entryCount: number;
  loadStatus: RequestStatus;
}

export type IRoleTableLoaderLogic = LogicWrapper<
  MakeOwnLogicType<{
    actions: Actions;
    values: Values;
  }>
>;

export namespace IRoleTableLoaderLogic {
  export const $: interfaces.ServiceIdentifier<IRoleTableLoaderLogic> = Symbol(
    'IRoleTableLoaderLogic',
  );
}
