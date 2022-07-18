import { interfaces } from 'inversify';
import { Logic, LogicWrapper } from 'kea';

interface ILogin extends Logic {
  readonly actions: {};
  readonly values: {};
}

export type ILoginLogic = LogicWrapper<ILogin>;

export namespace ILoginLogic {
  export const $: interfaces.ServiceIdentifier<ILoginLogic> =
    Symbol('ILoginLogic');
}
