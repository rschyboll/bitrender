/* eslint-disable @typescript-eslint/no-explicit-any */
import { IRouteValidators } from '../interfaces/route';
import { Validators } from './base';

export class RouteValidators extends Validators implements IRouteValidators {
  public routeStateHasLastPage(state: unknown): state is { lastPage: string } {
    if (
      typeof state == 'object' &&
      state != null &&
      'lastPage' in state &&
      typeof (state as any)['lastPage'] == 'string'
    ) {
      return true;
    }
    return false;
  }
}
