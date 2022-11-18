import type { interfaces } from 'inversify';
import type { LogicWrapper } from 'kea';

import type { MakeOwnLogicType } from '@/logic/types/makeLogic';
import type { RequestStatus } from '@/services';
import type { MRole } from '@/types/models';

interface Actions {
  setPermissionSelected: (
    permission: MRole.Permission,
    checked: boolean,
  ) => { permission: MRole.Permission; checked: boolean };
  setName: (name: string) => { name: string };
  setDefault: (isDefault: true | null) => { isDefault: true | null };
  save: true;
}

interface Values {
  selectedPermissions: Set<MRole.Permission>;
  name: string;
  isDefault: true | null;
  saveStatus: RequestStatus;
  nameTooShort: boolean;
  nameTaken: boolean;
}

export type ICreateRoleLogic = LogicWrapper<
  MakeOwnLogicType<{
    actions: Actions;
    values: Values;
  }>
>;

export namespace ICreateRoleLogic {
  export const $: interfaces.ServiceIdentifier<ICreateRoleLogic> =
    Symbol('ICreateRoleLogic');
}
