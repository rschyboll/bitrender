import { interfaces } from 'inversify';
import { Logic, LogicWrapper } from 'kea';

import { UserView } from '@/types/user';

interface IApp extends Logic {
  readonly actions: {};
  readonly values: {
    appReady: boolean;
    currentUser: UserView | null;
  };
}

export type IAppLogic = LogicWrapper<IApp>;

export namespace IAppLogic {
  export const $: interfaces.ServiceIdentifier<IAppLogic> = Symbol('IAppLogic');
}
