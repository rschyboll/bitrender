// Generated by kea-typegen on Wed, 20 Jul 2022 17:50:30 GMT. DO NOT EDIT THIS FILE MANUALLY.

import type { Logic } from 'kea'

import type { IUserService } from '../../../services/interfaces/index'

export interface logicType extends Logic {
  actionCreators: {
    loadCurrentUser: () => {
      type: 'load current user (logic.core.app.index)';
      payload: {
        value: true;
      };
    };
    openApp: () => {
      type: 'open app (logic.core.app.index)';
      payload: {
        value: true;
      };
    };
    openLoginPage: () => {
      type: 'open login page (logic.core.app.index)';
      payload: {
        value: true;
      };
    };
    openRegisterPage: () => {
      type: 'open register page (logic.core.app.index)';
      payload: {
        value: true;
      };
    };
    openUsersPage: () => {
      type: 'open users page (logic.core.app.index)';
      payload: {
        value: true;
      };
    };
    openRolesPage: () => {
      type: 'open roles page (logic.core.app.index)';
      payload: {
        value: true;
      };
    };
    openErrorPage: () => {
      type: 'open error page (logic.core.app.index)';
      payload: {
        value: true;
      };
    };
  };
  actionKeys: {
    'load current user (logic.core.app.index)': 'loadCurrentUser';
    'open app (logic.core.app.index)': 'openApp';
    'open login page (logic.core.app.index)': 'openLoginPage';
    'open register page (logic.core.app.index)': 'openRegisterPage';
    'open users page (logic.core.app.index)': 'openUsersPage';
    'open roles page (logic.core.app.index)': 'openRolesPage';
    'open error page (logic.core.app.index)': 'openErrorPage';
  };
  actionTypes: {
    loadCurrentUser: 'load current user (logic.core.app.index)';
    openApp: 'open app (logic.core.app.index)';
    openLoginPage: 'open login page (logic.core.app.index)';
    openRegisterPage: 'open register page (logic.core.app.index)';
    openUsersPage: 'open users page (logic.core.app.index)';
    openRolesPage: 'open roles page (logic.core.app.index)';
    openErrorPage: 'open error page (logic.core.app.index)';
  };
  actions: {
    loadCurrentUser: () => void;
    openApp: () => void;
    openLoginPage: () => void;
    openRegisterPage: () => void;
    openUsersPage: () => void;
    openRolesPage: () => void;
    openErrorPage: () => void;
  };
  defaults: {};
  events: {};
  key: undefined;
  listeners: {
    loadCurrentUser: ((
      action: {
        type: 'load current user (logic.core.app.index)';
        payload: {
          value: true;
        };
      },
      previousState: any,
    ) => void | Promise<void>)[];
  };
  path: ['logic', 'core', 'app', 'index'];
  pathString: 'logic.core.app.index';
  props: {
    deps: {
      userService: IUserService;
    };
  };
  reducer: (state: any, action: any, fullState: any) => {};
  reducers: {};
  selector: (state: any) => {};
  selectors: {};
  sharedListeners: {};
  values: {};
  _isKea: true;
  _isKeaWithKey: false;
}
