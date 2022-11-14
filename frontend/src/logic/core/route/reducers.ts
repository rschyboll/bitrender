import type { ReducersDef } from '@/logic';
import { history } from '@/pages/router';

import type { RouteLogicType } from './type';

export const Reducers: ReducersDef<RouteLogicType> = {
  currentLocation: [
    { ...history.location },
    {
      updateLocationState: (_, { location }) => {
        return { ...location };
      },
    },
  ],
};
