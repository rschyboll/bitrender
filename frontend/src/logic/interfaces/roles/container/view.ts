import type { interfaces } from 'inversify';

import type { MakeContainerBuilderLogicInterface } from '@/logic/builders';
import type { MRole } from '@/types/models';

export type IRoleViewContainerLogic =
  MakeContainerBuilderLogicInterface<MRole.View>;

export namespace IRoleViewContainerLogic {
  export const $: interfaces.ServiceIdentifier<IRoleViewContainerLogic> =
    Symbol('IRoleViewContainerLogic');
}
