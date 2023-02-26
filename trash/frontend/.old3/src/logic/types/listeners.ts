/* eslint-disable @typescript-eslint/no-explicit-any, @typescript-eslint/ban-types*/
import type { ListenerDefinitions, ListenerFunction } from 'kea';

import type { MakeOwnLogicType } from './makeLogic';

export type ListenersDef<Logic extends MakeOwnLogicType> =
  | ((logic: Logic) => ListenerDefinitions<Logic>)
  | ListenerDefinitions<Logic>;

export type SharedListenersDef<Logic extends MakeOwnLogicType> =
  | ((logic: Logic) => Record<keyof Logic['sharedListeners'], ListenerFunction>)
  | Record<keyof Logic['sharedListeners'], ListenerFunction>;
