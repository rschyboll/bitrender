import { interfaces } from 'inversify';
import { LogicWrapper } from 'kea';

import type { MakeOwnLogicType } from '@/logic/types';

interface Reducers {
  value: number;
}

interface Props {
  key: string;
}

export type ITestSingleLogicType = LogicWrapper<
  MakeOwnLogicType<{
    reducers: Reducers;
    props: Props;
  }>
>;

export namespace ITestSingleLogicType {
  export const $: interfaces.ServiceIdentifier<ITestSingleLogicType> = Symbol(
    'ITestSingleLogicType',
  );
}
