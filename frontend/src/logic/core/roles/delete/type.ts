import type { MakeOwnLogicType } from '@/logic';
import type { MakeRequestsBuilderLogicType } from '@/logic/builders/requests';
import type {
  IRoleUserCountLoaderLogic,
  IRoleViewLoaderLogic,
} from '@/logic/interfaces';
import type { ErrorResponse, RequestStatus } from '@/services';
import type { IRoleService } from '@/services/interfaces';
import type { MRole } from '@/types/models';

interface Selectors {
  id: (id: string) => string;
  view: (view: MRole.View | null) => MRole.View | null;
  viewLoadStatus: (status: RequestStatus) => RequestStatus;
  viewLoadError: (
    error: ErrorResponse['error'] | null,
  ) => ErrorResponse['error'] | null;
  userCount: (userCounts: number | null) => number | null;
  userCountLoadStatus: (status: RequestStatus) => RequestStatus;
  userCountLoadError: (
    error: ErrorResponse['error'] | null,
  ) => ErrorResponse['error'] | null;
}

interface Deps {
  roleService: IRoleService;
  roleViewLoaderLogic: IRoleViewLoaderLogic;
  roleUserCountLoaderLogic: IRoleUserCountLoaderLogic;
}

interface Props {
  id: string;
}

interface Requests {
  delete: IRoleService['delete'];
}

export type RoleDeleteLogic = MakeOwnLogicType<{
  selectors: Selectors;
  deps: Deps;
  props: Props;
}> &
  MakeRequestsBuilderLogicType<Requests>;
