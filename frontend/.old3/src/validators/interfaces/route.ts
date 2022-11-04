import { interfaces } from 'inversify';
import { Location } from 'react-router-dom';

export interface IRouteValidators {
  stateHasLastLocation: (state: unknown) => state is { lastLocation: Location };
}

export namespace IRouteValidators {
  export const $: interfaces.ServiceIdentifier<IRouteValidators> =
    Symbol('IRouteValidators');
}
