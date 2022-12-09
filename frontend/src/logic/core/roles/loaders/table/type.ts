import type { IRoleConverters } from '@/converters/interfaces';
import type { MakeOwnLogicType } from '@/logic';
import type { MakeRequestsBuilderLogicType } from '@/logic/builders';
import type { IRoleViewContainerLogic } from '@/logic/interfaces';
import type { IRoleService } from '@/services/interfaces';
import type { MRole } from '@/types/models';

interface Actions {
  setLoadedEntryIds: (entryIds: string[] | Set<string>) => {
    entryIds: string[] | Set<string>;
  };
  setEntryRowCount: (rowCount: number) => { rowCount: number };
}

interface Reducers {
  loadedEntryIds: Set<string>;
  entryCount: number;
}

interface Selectors {
  entries: (
    views: Map<string, MRole.View>,
    loadedEntryIds: Set<string>,
  ) => MRole.TableView[];
}

interface Deps {
  roleService: IRoleService;
  roleConverters: IRoleConverters;
  roleViewContainerLogic: IRoleViewContainerLogic;
}

interface Requests {
  load: IRoleService['getTable'];
}

export type RoleTableLoaderLogic = MakeOwnLogicType<{
  actions: Actions;
  reducers: Reducers;
  selectors: Selectors;
  deps: Deps;
}> &
  MakeRequestsBuilderLogicType<Requests>;
