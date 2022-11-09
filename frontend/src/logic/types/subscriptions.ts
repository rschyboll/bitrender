import type { Subscription } from 'kea-subscriptions';

import type { MakeOwnLogicType } from './makeLogic';

type SubscriptionDefinitions<Logic extends MakeOwnLogicType> = Partial<
  Record<keyof Logic['values'], Subscription>
>;

export type SubscriptionsDef<Logic extends MakeOwnLogicType> =
  | ((logic: Logic) => SubscriptionDefinitions<Logic>)
  | SubscriptionDefinitions<Logic>;
