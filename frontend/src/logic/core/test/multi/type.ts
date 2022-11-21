import { MakeReselectorsBuilderLogicType } from '@/logic/builders';
import { ITestSingleLogicType } from '@/logic/interfaces';
import type { MakeOwnLogicType } from '@/logic/types';

interface Deps {
  testSingleLogic: ITestSingleLogicType;
}

interface Reselectors {
  values: (test: string) => number[];
}

interface Props {}

interface Selectors {
  keys: () => string[];
}

export type TestMultiLogicType = MakeOwnLogicType<{
  deps: Deps;
  props: Props;
  selectors: Selectors;
}> &
  MakeReselectorsBuilderLogicType<Reselectors>;
