import type { KeyType } from 'kea';

import type { MakeOwnLogicType } from '@/logic';
import type { MakeRequestsBuilderLogicType } from '@/logic/builders';
import type { IRoleViewContainerLogic } from '@/logic/interfaces';
import type { IRoleService } from '@/services/interfaces';
import type { MRole } from '@/types/models';

interface Actions {
  addLoadedEntryIds: (
    entryIds: string[] | Set<string>,
    offset: number,
  ) => {
    entryIds: string[] | Set<string>;
    offset: number;
  };
  setEntryRowCount: (rowCount: number) => { rowCount: number };
  refresh: true;
}

interface Reducers {
  loadedEntryIds: Map<number, string>;
  entryCount: number | null;
}

interface Selectors {
  entries: (
    views: Map<string, MRole.View>,
    loadedEntryIds: Map<number, string>,
    entryCount: number | null,
  ) => MRole.View[];
}

interface Deps {
  roleService: IRoleService;
  roleViewContainerLogic: IRoleViewContainerLogic;
}

interface Props {
  beginning: number;
  end: number;
  key: KeyType;
}

interface Requests {
  load: IRoleService['getTable'];
}

export type RoleVirtualLoaderLogic = MakeOwnLogicType<{
  actions: Actions;
  reducers: Reducers;
  selectors: Selectors;
  deps: Deps;
  props: Props;
}> &
  MakeRequestsBuilderLogicType<Requests>;
