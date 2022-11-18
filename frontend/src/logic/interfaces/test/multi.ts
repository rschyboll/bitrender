import { interfaces } from 'inversify';

import type { MakeOwnLogicType } from '@/logic/types';

export type ITestMultiLogicType = MakeOwnLogicType<{}>;

export namespace ITestMultiLogicType {
  export const $: interfaces.ServiceIdentifier<ITestMultiLogicType> = Symbol(
    'ITestMultiLogicType',
  );
}
