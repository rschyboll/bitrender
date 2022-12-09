import type { MakeOwnLogicType } from '@/logic';
import type { MakeRequestsBuilderLogicType } from '@/logic/builders';
import type { IRoleViewContainerLogic } from '@/logic/interfaces';
import type { IRoleService } from '@/services/interfaces';
import type { MRole } from '@/types/models';

interface Selectors {
  id: (id: string) => string;
  entry: (views: Map<string, MRole.View>, uuid: string) => MRole.View | null;
}

interface Props {
  id: string;
}

interface Deps {
  roleService: IRoleService;
  roleViewContainerLogic: IRoleViewContainerLogic;
}

interface Requests {
  load: IRoleService['getById'];
}

export type RoleViewLoaderLogic = MakeOwnLogicType<{
  selectors: Selectors;
  props: Props;
  deps: Deps;
}> &
  MakeRequestsBuilderLogicType<Requests>;
