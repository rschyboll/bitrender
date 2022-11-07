import { RequestStatus } from "@/types/service";
import { MakeOwnLogicType } from "@/logic/types/makeLogic";

interface Actions {
  addNewRole: true;
  addNewRoleFailure: (searchString: string) => { searchString: string };
  addNewRoleSuccess: true;
  updateRole: true;
  updateRoleSuccess: true;
  updateRoleFailure: true;
}

interface Reducers {
  addNewRoleStatus: RequestStatus;
}

interface Selectors {}

export type RolesTableLogic = MakeOwnLogicType<{
  actions: Actions;
}>;