import { RequestStatus } from "@/services/enums";
import { IRouteLogic } from "@/logic/interfaces";
import { MakeOwnLogicType } from "@/logic/types/makeLogic";
import { IUserService } from "@/services/interfaces";
import { IUserValidators } from "@/validators/interfaces";

interface Actions {
  checkLoggedIn: true;
  login: (
    username: string,
    password: string
  ) => { username: string; password: string };
  loginSuccess: true;
  loginFailure: (errorDetail?: unknown) => { errorDetail?: unknown };
  logout: true;
  logoutSuccess: true;
  logoutFailure: (errorDetail?: unknown) => { errorDetail?: unknown };
  register: (
    email: string,
    username: string,
    password: string
  ) => {
    email: string;
    username: string;
    password: string;
  };
  registerSuccess: true;
  registerFailure: (errorDetail?: unknown) => { errorDetail?: unknown };
  registerResetStatus: true;
  setRegisterWeakPassword: (weakPassword: boolean) => { weakPassword: boolean };
  setRegisterWrongEmail: (wrongEmail: boolean) => { wrongEmail: boolean };
}

interface Reducers {
  loginStatus: RequestStatus;
  loginErrorDetail: null | unknown;
  logoutStatus: RequestStatus;
  registerStatus: RequestStatus;
  registerErrorDetail: null | unknown;
  registerWeakPassword: boolean;
  registerWrongEmail: boolean;
}

interface Deps {
  routeLogic: IRouteLogic;
  userService: IUserService;
  userValidators: IUserValidators;
}

export type AuthLogic = MakeOwnLogicType<{
  reducers: Reducers;
  actions: Actions;
  deps: Deps;
}>;
