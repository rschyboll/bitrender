import { interfaces } from 'inversify';
import { Logic, LogicWrapper } from 'kea';

interface IApp extends Logic {
  readonly actions: {};
  readonly values: {};
}

export type IAppLogic = LogicWrapper<IApp>;

export namespace IAppLogic {
  export const $: interfaces.ServiceIdentifier<IAppLogic> = Symbol('IAppLogic');
}
