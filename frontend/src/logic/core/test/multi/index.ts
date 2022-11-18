import { kea, path } from 'kea';

import type { TestMultiLogicType } from './type';

const logic = kea<TestMultiLogicType>([path(['test', 'multi'])]);

export const testMultiLogic = logic;
