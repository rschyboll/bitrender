import type { IRoleConverters } from '@/converters/interfaces';
import type { MakeOwnLogicType } from '@/logic';
import type { IRouteLogic } from '@/logic/interfaces';
import type { RequestStatus } from '@/services';
import type { IRoleService } from '@/services/interfaces';
import { ListRequestInput } from '@/services/messages/list';
import type { MRole } from '@/types/models';

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
  amountOfRecords: number;
}

interface Selectors {
  values: (roles: MRole.View[]) => MRole.TableView[];
  searchString: (
    localSearchString: string | null,
    hashParams: Record<string, unknown>,
  ) => string;
  rowsPerPage: (hashParams: Record<string, unknown>) => number;
  currentPage: (hashParams: Record<string, unknown>) => number;
  listRequestInput: (
    currentPage: number,
    rowsPerPage: number,
    searchString: string,
  ) => ListRequestInput<MRole.Columns>;
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
