import { kea, path } from 'kea';

import { deps, reselectors } from '@/logic/builders';
import { ITestSingleLogicType } from '@/logic/interfaces';

import type { TestMultiLogicType } from './type';

const logic = kea<TestMultiLogicType>([
  path(['test', 'multi']),
  deps({ testSingleLogic: ITestSingleLogicType.$ }),
  reselectors(({ deps }) => ({
    values: [
      (selectors) => selectors.keys,
      (id) => deps.testSingleLogic({ key: id }).selectors.value,
    ],
  })),
]);

export const testMultiLogic = logic;
