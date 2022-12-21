import type { interfaces } from 'inversify';
import type { LogicWrapper } from 'kea';

import type { MakeOwnLogicType } from '@/logic/types/makeLogic';
import type { ErrorResponse, RequestStatus } from '@/services';
import type { MRole } from '@/types/models';

interface Values {
  view: MRole.View | null;
  viewLoadStatus: RequestStatus;
  viewLoadError: ErrorResponse['error'] | null;
  userCount: number | null;
  userCountLoadStatus: RequestStatus;
  userCountLoadError: ErrorResponse['error'] | null;
}

interface Props {
  id: string;
}

export type IRoleDeleteLogic = LogicWrapper<
  MakeOwnLogicType<{
    values: Values;
    props: Props;
  }>
>;

export namespace IRoleDeleteLogic {
  export const $: interfaces.ServiceIdentifier<IRoleDeleteLogic> =
    Symbol('IRoleDeleteLogic');
}
