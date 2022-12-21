import type { SubscriptionsDef } from '@/logic';

import type { RoleUserCountLoaderLogic } from './type';

export const Subscriptions: SubscriptionsDef<RoleUserCountLoaderLogic> = ({
  actions,
  values,
}) => ({
  entry: (value) => {
    if (value == null) {
      actions.load({ id: values.id });
    }
  },
});
