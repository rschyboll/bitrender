import type { IRoleConverters } from '@/converters/interfaces';
import type { IRouteLogic } from '@/logic/interfaces';

import type { RequestStatus } from '@/services';

import type { MRole } from '@/types/models';
import type { IRoleService } from '@/services/interfaces';
import type { MakeOwnLogicType } from '@/logic';

interface Actions {
  refresh: true;
  load: true;
  loadSuccess: (
    roles: MRole.View[],
    rowCount: number,
  ) => { roles: MRole.View[]; rowCount: number };
  loadFailure: true;
  setSearchString: (searchString: string) => { searchString: string };
  setCurrentPage: (currentPage: number) => { currentPage: number };
  setLocalSearchString: (searchString: string) => { searchString: string };
  setRowsPerPage: (rowsPerPage: number) => { rowsPerPage: number };
}

interface Reducers {
  localSearchString: string | null;
  loadState: RequestStatus;
  roles: MRole.View[];
}

interface Selectors {
  values: (roles: MRole.View[]) => MRole.TableView[];
}

interface Deps {
  routeLogic: IRouteLogic;
  roleService: IRoleService;
  roleConverters: IRoleConverters;
}

export type RolesTableLogic = MakeOwnLogicType<{
  actions: Actions;
  reducers: Reducers;
  selectors: Selectors;
  deps: Deps;
}>;
