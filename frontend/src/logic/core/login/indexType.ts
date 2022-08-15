// Generated by kea-typegen on Mon, 15 Aug 2022 11:06:50 GMT. DO NOT EDIT THIS FILE MANUALLY.

import type { Logic } from 'kea'

import type { IRouteLogic } from '../../interfaces/route'
import type { IUserService } from '../../../services/interfaces/index'
import type { IUserValidators } from '../../../validators/interfaces/index'
import type { RequestStatus } from '../../../types/service'

export interface logicType extends Logic {
  actionCreators: {
    checkLoggedIn: () => {
      type: 'check logged in (login)';
      payload: {
        value: true;
      };
    };
    login: (
      username: string,
      password: string,
    ) => {
      type: 'login (login)';
      payload: {
        username: string;
        password: string;
      };
    };
    loginSuccess: () => {
      type: 'login success (login)';
      payload: {
        value: true;
      };
    };
    loginFailure: (errorDetail?: unknown) => {
      type: 'login failure (login)';
      payload: {
        errorDetail: unknown;
      };
    };
    logout: () => {
      type: 'logout (login)';
      payload: {
        value: true;
      };
    };
    logoutSuccess: () => {
      type: 'logout success (login)';
      payload: {
        value: true;
      };
    };
    logoutFailure: (errorDetail?: unknown) => {
      type: 'logout failure (login)';
      payload: {
        errorDetail: unknown;
      };
    };
    register: (
      email: string,
      username: string,
      password: string,
    ) => {
      type: 'register (login)';
      payload: {
        email: string;
        username: string;
        password: string;
      };
    };
    registerSuccess: () => {
      type: 'register success (login)';
      payload: {
        value: true;
      };
    };
    registerFailure: (errorDetail?: unknown) => {
      type: 'register failure (login)';
      payload: {
        errorDetail: unknown;
      };
    };
    registerResetStatus: () => {
      type: 'register reset status (login)';
      payload: {
        value: true;
      };
    };
    setRegisterWeakPassword: (weakPassword: boolean) => {
      type: 'set register weak password (login)';
      payload: {
        weakPassword: boolean;
      };
    };
    setRegisterWrongEmail: (wrongEmail: boolean) => {
      type: 'set register wrong email (login)';
      payload: {
        wrongEmail: boolean;
      };
    };
  };
  actionKeys: {
    'check logged in (login)': 'checkLoggedIn';
    'login (login)': 'login';
    'login success (login)': 'loginSuccess';
    'login failure (login)': 'loginFailure';
    'logout (login)': 'logout';
    'logout success (login)': 'logoutSuccess';
    'logout failure (login)': 'logoutFailure';
    'register (login)': 'register';
    'register success (login)': 'registerSuccess';
    'register failure (login)': 'registerFailure';
    'register reset status (login)': 'registerResetStatus';
    'set register weak password (login)': 'setRegisterWeakPassword';
    'set register wrong email (login)': 'setRegisterWrongEmail';
  };
  actionTypes: {
    checkLoggedIn: 'check logged in (login)';
    login: 'login (login)';
    loginSuccess: 'login success (login)';
    loginFailure: 'login failure (login)';
    logout: 'logout (login)';
    logoutSuccess: 'logout success (login)';
    logoutFailure: 'logout failure (login)';
    register: 'register (login)';
    registerSuccess: 'register success (login)';
    registerFailure: 'register failure (login)';
    registerResetStatus: 'register reset status (login)';
    setRegisterWeakPassword: 'set register weak password (login)';
    setRegisterWrongEmail: 'set register wrong email (login)';
  };
  actions: {
    checkLoggedIn: () => void;
    login: (username: string, password: string) => void;
    loginSuccess: () => void;
    loginFailure: (errorDetail?: unknown) => void;
    logout: () => void;
    logoutSuccess: () => void;
    logoutFailure: (errorDetail?: unknown) => void;
    register: (email: string, username: string, password: string) => void;
    registerSuccess: () => void;
    registerFailure: (errorDetail?: unknown) => void;
    registerResetStatus: () => void;
    setRegisterWeakPassword: (weakPassword: boolean) => void;
    setRegisterWrongEmail: (wrongEmail: boolean) => void;
  };
  defaults: {
    loginStatus: RequestStatus;
    loginErrorDetail: null | unknown;
    logoutStatus: RequestStatus;
    registerStatus: RequestStatus;
    registerWeakPassword: boolean;
    registerWrongEmail: boolean;
    registerErrorDetail: null | unknown;
  };
  events: {};
  key: undefined;
  listeners: {
    checkLoggedIn: ((
      action: {
        type: 'check logged in (login)';
        payload: {
          value: true;
        };
      },
      previousState: any,
    ) => void | Promise<void>)[];
    login: ((
      action: {
        type: 'login (login)';
        payload: {
          username: string;
          password: string;
        };
      },
      previousState: any,
    ) => void | Promise<void>)[];
    loginSuccess: ((
      action: {
        type: 'login success (login)';
        payload: {
          value: true;
        };
      },
      previousState: any,
    ) => void | Promise<void>)[];
    register: ((
      action: {
        type: 'register (login)';
        payload: {
          email: string;
          username: string;
          password: string;
        };
      },
      previousState: any,
    ) => void | Promise<void>)[];
  };
  path: ['login'];
  pathString: 'login';
  props: {
    deps: {
      routeLogic: IRouteLogic;
      userService: IUserService;
      userValidators: IUserValidators;
    };
  };
  reducer: (
    state: any,
    action: any,
    fullState: any,
  ) => {
    loginStatus: RequestStatus;
    loginErrorDetail: null | unknown;
    logoutStatus: RequestStatus;
    registerStatus: RequestStatus;
    registerWeakPassword: boolean;
    registerWrongEmail: boolean;
    registerErrorDetail: null | unknown;
  };
  reducers: {
    loginStatus: (
      state: RequestStatus,
      action: any,
      fullState: any,
    ) => RequestStatus;
    loginErrorDetail: (
      state: null | unknown,
      action: any,
      fullState: any,
    ) => null | unknown;
    logoutStatus: (
      state: RequestStatus,
      action: any,
      fullState: any,
    ) => RequestStatus;
    registerStatus: (
      state: RequestStatus,
      action: any,
      fullState: any,
    ) => RequestStatus;
    registerWeakPassword: (
      state: boolean,
      action: any,
      fullState: any,
    ) => boolean;
    registerWrongEmail: (
      state: boolean,
      action: any,
      fullState: any,
    ) => boolean;
    registerErrorDetail: (
      state: null | unknown,
      action: any,
      fullState: any,
    ) => null | unknown;
  };
  selector: (state: any) => {
    loginStatus: RequestStatus;
    loginErrorDetail: null | unknown;
    logoutStatus: RequestStatus;
    registerStatus: RequestStatus;
    registerWeakPassword: boolean;
    registerWrongEmail: boolean;
    registerErrorDetail: null | unknown;
  };
  selectors: {
    loginStatus: (state: any, props?: any) => RequestStatus;
    loginErrorDetail: (state: any, props?: any) => null | unknown;
    logoutStatus: (state: any, props?: any) => RequestStatus;
    registerStatus: (state: any, props?: any) => RequestStatus;
    registerWeakPassword: (state: any, props?: any) => boolean;
    registerWrongEmail: (state: any, props?: any) => boolean;
    registerErrorDetail: (state: any, props?: any) => null | unknown;
  };
  sharedListeners: {};
  values: {
    loginStatus: RequestStatus;
    loginErrorDetail: null | unknown;
    logoutStatus: RequestStatus;
    registerStatus: RequestStatus;
    registerWeakPassword: boolean;
    registerWrongEmail: boolean;
    registerErrorDetail: null | unknown;
  };
  _isKea: true;
  _isKeaWithKey: false;
}
