import type { MakeOwnLogicType } from '@/logic';
import { MakeRequestsBuilderLogicType } from '@/logic/builders/requests';
import { RequestStatus } from '@/services';
import { IRoleService } from '@/services/interfaces';
import { MRole } from '@/types/models';

interface Actions {
  setPermissionSelected: (
    permission: MRole.Permission,
    checked: boolean,
  ) => { permission: MRole.Permission; checked: boolean };
  setName: (name: string) => { name: string };
  setDefault: (isDefault: true | null) => { isDefault: true | null };
  save: true;
}

interface Reducers {
  selectedPermissions: Set<MRole.Permission>;
  name: string;
  isDefault: true | null;
}

interface Selectors {
  saveStatus: (createStatus: RequestStatus) => RequestStatus;
}

interface Deps {
  roleService: IRoleService;
}

interface Requests {
  create: IRoleService['create'];
}

export type CreateRoleLogic = MakeOwnLogicType<{
  actions: Actions;
  reducers: Reducers;
  selectors: Selectors;
  deps: Deps;
}> &
  MakeRequestsBuilderLogicType<Requests>;
