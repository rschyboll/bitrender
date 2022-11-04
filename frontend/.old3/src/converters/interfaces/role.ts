import { interfaces } from 'inversify';

import { RoleTableView, RoleView } from '@/schemas/role';

export interface IRoleConverters {
  viewToTableView: (view: RoleView) => RoleTableView;
}

export namespace IRoleConverters {
  export const $: interfaces.ServiceIdentifier<IRoleConverters> =
    Symbol('IRoleConverters');
}
