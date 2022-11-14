import type { ListenersDef } from '@/logic/types';
import { ApiErrorCodes, ServiceErrorType } from '@/services/enums';
import { sleep } from '@/utils/async';

import type { AuthLogic } from './type';

export const Listeners: ListenersDef<AuthLogic> = ({
  actions,
  deps,
  values,
}) => ({
  checkLoggedIn: async () => {
    const response = await deps.userService.logged();
    if (response.success && response.data) {
      deps.routeLogic.actions.openApp();
    } else if (!response.success) {
      await sleep(1000);
      actions.checkLoggedIn();
    }
  },
  login: async ({ username, password }) => {
    const response = await deps.userService.login(username, password);
    if (response.success) {
      actions.loginSuccess();
    } else {
      if ('detail' in response.error) {
        if (response.error.detail == ApiErrorCodes.UserNotVerified) {
          deps.routeLogic.actions.openVerifyPage(username);
        }
        actions.loginFailure(response.error.detail);
      } else {
        actions.loginFailure();
      }
    }
  },
  loginSuccess: () => {
    deps.routeLogic.actions.returnToBeforeLogin();
  },
  register: async ({ email, username, password }) => {
    if (!deps.userValidators.validateUserPasswordStrength(password)) {
      actions.setRegisterWeakPassword(true);
      actions.registerResetStatus();
      return;
    } else if (values.registerWeakPassword) {
      actions.setRegisterWeakPassword(false);
    }

    if (!deps.userValidators.validateUserEmail(email)) {
      actions.setRegisterWrongEmail(true);
      actions.registerResetStatus();
      return;
    } else if (values.registerWrongEmail) {
      actions.setRegisterWrongEmail(false);
    }

    const response = await deps.userService.register({
      email,
      username,
      password,
    });
    if (response.success) {
      actions.registerSuccess();
    } else {
      if ('detail' in response.error) {
        actions.registerFailure(response.error.detail);
      } else {
        actions.registerFailure();
      }
    }
  },
  logout: async () => {
    const response = await deps.userService.logout();
    if (response.success) {
      deps.routeLogic.actions.openLoginPage();
    } else {
      if (
        response.error.type == ServiceErrorType.ApiError &&
        response.error.detail == ApiErrorCodes.NotAuthenticated
      ) {
        deps.routeLogic.actions.openLoginPage();
      }
    }
  },
});
