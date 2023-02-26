/* eslint-disable @typescript-eslint/no-explicit-any */
import { Location } from 'react-router-dom';

import { IRouteValidators } from '../interfaces/route';
import { Validators } from './base';

export class RouteValidators extends Validators implements IRouteValidators {
  public stateHasLastLocation(state: any): state is { lastLocation: Location } {
    return (
      typeof state == 'object' &&
      state != null &&
      'lastLocation' in state &&
      state['lastLocation'] != null &&
      'state' in state['lastLocation'] &&
      state['lastLocation']['state'] != null &&
      'pathName' in state['lastLocation'] &&
      typeof state['lastLocation']['pathName'] == 'string'
    );
  }
}
