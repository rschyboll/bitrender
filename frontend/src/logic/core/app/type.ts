import { MakeRequestsBuilderLogicType } from '@/logic/builders/requests';
import { MakeOwnLogicType } from '@/logic/types';
import { UserView } from '@/schemas/user';
import { IUserService } from '@/services/interfaces';

interface Reducers {
  appReady: boolean;
  currentUser: UserView | null;
}

interface Deps {
  userService: IUserService;
}

interface Requests {
  loadCurrentUser: IUserService['getCurrentUser'];
}

export type AppLogicType = MakeOwnLogicType<{
  reducers: Reducers;
  deps: Deps;
}> &
  MakeRequestsBuilderLogicType<Requests>;
