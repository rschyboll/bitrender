import type { SelectorsDef } from '@/logic/types';

import type { CreateRoleLogic } from './type';

export const Selectors: SelectorsDef<CreateRoleLogic> = () => ({
  saveStatus: [
    (selectors) => [selectors.createStatus],
    (createStatus) => {
      return createStatus;
    },
  ],
});
