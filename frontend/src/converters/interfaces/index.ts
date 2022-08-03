import { interfaces } from 'inversify';

export { IUserConverters } from './user';

export interface IUtilityConverters {
  camelCaseKeysToSnakeCase: (o: unknown) => unknown;
  snakeCaseKeysToCamelCase: (o: unknown) => unknown;
}

export namespace IUtilityConverters {
  export const $: interfaces.ServiceIdentifier<IUtilityConverters> =
    Symbol('IUtilityConverters');
}
