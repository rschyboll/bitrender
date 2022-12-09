import type { MakeOwnLogicType } from '@/logic';
import type { MakeRequestsBuilderLogicType } from '@/logic/builders/requests';
import type { ErrorResponse, RequestStatus } from '@/services';
import type { IRoleService } from '@/services/interfaces';
import type { MRole } from '@/types/models';

interface Actions {}

interface Reducers {}

interface Selectors {}

interface Deps {
  roleService: IRoleService;
}

interface Requests {
  create: IRoleService['create'];
}

export type RoleCreateLogic = MakeOwnLogicType<{
  actions: Actions;
  reducers: Reducers;
  selectors: Selectors;
  deps: Deps;
}> &
  MakeRequestsBuilderLogicType<Requests>;
