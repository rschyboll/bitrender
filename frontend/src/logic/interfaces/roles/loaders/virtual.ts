import type { interfaces } from 'inversify';
import type { KeyType, LogicWrapper } from 'kea';

import type { MakeOwnLogicType } from '@/logic/types/makeLogic';
import type { RequestStatus } from '@/services';
import type { MRole } from '@/types/models';

interface Values {
  entries: MRole.View[];
  entryCount: number;
  loadStatus: RequestStatus;
}

interface Props {
  beginning: number;
  end: number;
  key: KeyType;
}

export type IRoleVirtualLoaderLogic = LogicWrapper<
  MakeOwnLogicType<{
    values: Values;
    props: Props;
  }>
>;

export namespace IRoleVirtualLoaderLogic {
  export const $: interfaces.ServiceIdentifier<IRoleVirtualLoaderLogic> =
    Symbol('IRoleVirtualLoaderLogic');
}
