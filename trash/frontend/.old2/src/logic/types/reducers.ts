import type { ReducerDefinitions } from 'kea';

import type { MakeOwnLogicType } from './makeLogic';

export type ReducersDef<Logic extends MakeOwnLogicType> =
  | ((logic: Logic) => ReducerDefinitions<Logic>)
  | ReducerDefinitions<Logic>;
