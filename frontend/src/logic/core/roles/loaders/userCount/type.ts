import type { MakeOwnLogicType } from '@/logic';
import type { MakeRequestsBuilderLogicType } from '@/logic/builders';
import type { IRoleUserCountContainerLogic } from '@/logic/interfaces';
import type { IRoleService } from '@/services/interfaces';
import type { MRole } from '@/types/models';

interface Actions {
  refresh: true;
}

interface Selectors {
  entry: (entries: Map<string, number>, id: string) => number | null;
  id: (id: string) => string;
}

interface Deps {
  roleService: IRoleService;
  roleUserCountContainerLogic: IRoleUserCountContainerLogic;
}

interface Requests {
  load: IRoleService['getUserCount'];
}

interface Props {
  id: string;
}

export type RoleUserCountLoaderLogic = MakeOwnLogicType<{
  actions: Actions;
  selectors: Selectors;
  deps: Deps;
  props: Props;
}> &
  MakeRequestsBuilderLogicType<Requests>;
