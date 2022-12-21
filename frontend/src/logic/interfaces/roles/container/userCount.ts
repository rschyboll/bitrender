import type { interfaces } from 'inversify';

import type { MakeContainerBuilderLogicInterface } from '@/logic/builders/container';

export type IRoleUserCountContainerLogic =
  MakeContainerBuilderLogicInterface<number>;

export namespace IRoleUserCountContainerLogic {
  export const $: interfaces.ServiceIdentifier<IRoleUserCountContainerLogic> =
    Symbol('IRoleUserCountContainerLogic');
}
