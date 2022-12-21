import type { interfaces } from 'inversify';
import type { LogicWrapper } from 'kea';

import type { MakeOwnLogicType } from '@/logic/types/makeLogic';
import type { ErrorResponse, RequestStatus } from '@/services';
import type { MRole } from '@/types/models';

interface Actions {
  load: (input: MRole.Messages.GetByIdInput) => {
    input: MRole.Messages.GetByIdInput;
  };
}

interface Values {
  entry: MRole.View | null;
  loadStatus: RequestStatus;
  loadError: ErrorResponse['error'] | null;
}

interface Props {
  id: string;
}

export type IRoleViewLoaderLogic = LogicWrapper<
  MakeOwnLogicType<{
    actions: Actions;
    values: Values;
    props: Props;
  }>
>;

export namespace IRoleViewLoaderLogic {
  export const $: interfaces.ServiceIdentifier<IRoleViewLoaderLogic> = Symbol(
    'IRoleViewLoaderLogic',
  );
}
