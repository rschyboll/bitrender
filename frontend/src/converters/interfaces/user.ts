import { interfaces } from 'inversify';

export interface IUserConverters {}

export namespace IUserConverters {
  export const $: interfaces.ServiceIdentifier<IUserConverters> =
    Symbol('IUserConverters');
}
