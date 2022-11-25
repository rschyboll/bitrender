import type { SelectorsDef } from '@/logic/types';

import type { TestMultiLogicType } from './type';

export const Selectors: SelectorsDef<TestMultiLogicType> = () => ({
  keys: [
    (_, p) => [p.keys],
    (keys) => {
      return keys;
    },
  ],
});
