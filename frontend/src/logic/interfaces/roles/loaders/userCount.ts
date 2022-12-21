import type { interfaces } from 'inversify';
import type { LogicWrapper } from 'kea';

import type { MakeOwnLogicType } from '@/logic/types/makeLogic';
import type { ErrorResponse, RequestStatus } from '@/services';
import type { MRole } from '@/types/models';

interface Actions {
  load: (input: MRole.Messages.GetUserCountInput) => {
    input: MRole.Messages.GetUserCountInput;
  };
}

interface Values {
  entry: number | null;
  loadStatus: RequestStatus;
  loadError: ErrorResponse['error'] | null;
}

interface Props {
  id: string;
}

export type IRoleUserCountLoaderLogic = LogicWrapper<
  MakeOwnLogicType<{
    actions: Actions;
    values: Values;
    props: Props;
  }>
>;

export namespace IRoleUserCountLoaderLogic {
  export const $: interfaces.ServiceIdentifier<IRoleUserCountLoaderLogic> =
    Symbol('IRoleUserCountLoaderLogic');
}
