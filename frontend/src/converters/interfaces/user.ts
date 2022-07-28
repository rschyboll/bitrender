import { interfaces } from 'inversify';

import { UserView, UserViewResponse } from '@/types/user';

export interface IUserConverters {
  userViewResponseToUserView(viewResponse: UserViewResponse): UserView;
}

export namespace IUserConverters {
  export const $: interfaces.ServiceIdentifier<IUserConverters> =
    Symbol('IUserConverters');
}
