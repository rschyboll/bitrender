import { MakeOwnLogicType } from '@/logic/types/makeLogic';

interface Actions {
  refresh: true;
  setSearchString: (searchString: string) => { searchString: string };
}

interface Reducers {}

interface Selectors {}

export type RolesTableLogic = MakeOwnLogicType<{
  actions: Actions;
}>;
