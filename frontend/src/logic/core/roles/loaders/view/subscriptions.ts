import type { SubscriptionsDef } from '@/logic';

import type { RoleViewLoaderLogic } from './type';

export const Subscriptions: SubscriptionsDef<RoleViewLoaderLogic> = ({
  actions,
  values,
}) => ({
  entry: (value) => {
    if (value == null) {
      actions.load({ id: values.id });
    }
  },
});
