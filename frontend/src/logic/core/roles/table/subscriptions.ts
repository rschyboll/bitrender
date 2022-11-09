import type { SubscriptionsDef } from '@/logic';

import type { RolesTableLogic } from './type';

export const Subscriptions: SubscriptionsDef<RolesTableLogic> = ({
  actions,
  values,
}) => ({
  listRequestInput: async () => {
    actions.refresh();
  },
  searchString: (value) => {
    if (value != values.localSearchString) {
      actions.setLocalSearchString(value);
    }
  },
});
