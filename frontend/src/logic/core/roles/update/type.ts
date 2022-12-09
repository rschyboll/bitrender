import type { MakeOwnLogicType } from '@/logic';
import type { MakeRequestsBuilderLogicType } from '@/logic/builders/requests';
import type { IRoleViewLoaderLogic } from '@/logic/interfaces';
import type { ErrorResponse, RequestStatus } from '@/services';
import type { IRoleService } from '@/services/interfaces';
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

interface Reducers {
  selectedPermissions: Set<MRole.Permission>;
  name: string;
  isDefault: true | null;
  saveClicked: boolean;
}

interface Selectors {
  saveStatus: (createStatus: RequestStatus) => RequestStatus;
  inputReady: (
    selectedPermissions: Reducers['selectedPermissions'],
    name: Reducers['name'],
    isDefault: Reducers['isDefault'],
  ) => boolean;
  nameTooShort: (name: string, saveClicked: boolean) => boolean;
  nameTaken: (
    createStatus: RequestStatus,
    createError: ErrorResponse['error'] | null,
  ) => boolean;
}

interface Props {
  id: string;
}

interface Deps {
  roleViewLoaderLogic: IRoleViewLoaderLogic;
  roleService: IRoleService;
}

interface Requests {
  create: IRoleService['create'];
}

export type RoleUpdateLogic = MakeOwnLogicType<{
  actions: Actions;
  reducers: Reducers;
  selectors: Selectors;
  props: Props;
  deps: Deps;
}> &
  MakeRequestsBuilderLogicType<Requests>;
