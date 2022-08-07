import { interfaces } from 'inversify';
import { Options } from 'ky';

export { IUserConverters } from './user';

export interface IUtilityConverters {
  requestToSnakeCase: (
    request: Request,
    options: Options,
  ) => Promise<Request | undefined>;
  responseToCamelCase: (
    _: unknown,
    __: unknown,
    response: Response,
  ) => Promise<Response | undefined>;
}

export namespace IUtilityConverters {
  export const $: interfaces.ServiceIdentifier<IUtilityConverters> =
    Symbol('IUtilityConverters');
}
