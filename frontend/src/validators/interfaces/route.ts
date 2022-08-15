import { interfaces } from 'inversify';

export interface IRouteValidators {
  routeStateHasLastPage: (state: unknown) => state is { lastPage: string };
}

export namespace IRouteValidators {
  export const $: interfaces.ServiceIdentifier<IRouteValidators> =
    Symbol('IRouteValidators');
}
