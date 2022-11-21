import { interfaces } from 'inversify';
import { LogicWrapper } from 'kea';

import type { MakeOwnLogicType } from '@/logic/types';

interface Props {
  keys: string[];
}

export type ITestMultiLogicType = LogicWrapper<
  MakeOwnLogicType<{ props: Props }>
>;

export namespace ITestMultiLogicType {
  export const $: interfaces.ServiceIdentifier<ITestMultiLogicType> = Symbol(
    'ITestMultiLogicType',
  );
}
