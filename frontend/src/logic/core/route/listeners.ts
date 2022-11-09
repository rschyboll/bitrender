import type { ListenersDef, SharedListenersDef } from '@/logic/types';

import type { RouteLogicType } from './type';

export const SharedListeners: SharedListenersDef<RouteLogicType> = ({
  values,
}) => ({});

export const Listeners: ListenersDef<RouteLogicType> = ({
  values,
  deps,
}) => ({});
