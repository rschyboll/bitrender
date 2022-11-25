import { kea, path, selectors } from 'kea';

import { deps, reselectors } from '@/logic/builders';
import { ITestSingleLogicType } from '@/logic/interfaces';

import { Selectors } from './selectors';
import type { TestMultiLogicType } from './type';

const logic = kea<TestMultiLogicType>([
  path(['test', 'multi']),
  deps({ testSingleLogic: ITestSingleLogicType.$ }),
  selectors(Selectors),
  reselectors(({ deps }) => ({
    values: [
      (selectors) => selectors.keys,
      (id) => deps.testSingleLogic({ key: id }).selectors.value,
    ],
  })),
]);

export const testMultiLogic = logic;
