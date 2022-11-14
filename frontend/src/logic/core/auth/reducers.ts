import type { ReducersDef } from '@/logic';
import { RequestStatus } from '@/services';

import type { AuthLogic } from './type';

export const Reducers: ReducersDef<AuthLogic> = {
  loginStatus: [
    RequestStatus.Idle,
    {
      login: () => RequestStatus.Idle,
      loginSuccess: () => RequestStatus.Success,
      loginFailure: () => RequestStatus.Failure,
    },
  ],
  loginErrorDetail: [
    null as null | unknown,
    {
      loginFailure: (_, { errorDetail }) =>
        errorDetail !== undefined ? errorDetail : null,
    },
  ],
  logoutStatus: [
    RequestStatus.Idle,
    {
      logout: () => RequestStatus.Idle,
      logoutSuccess: () => RequestStatus.Success,
      logoutFailure: () => RequestStatus.Failure,
    },
  ],
  registerStatus: [
    RequestStatus.Idle as RequestStatus,
    {
      register: () => RequestStatus.Idle,
      registerSuccess: () => RequestStatus.Success,
      registerFailure: () => RequestStatus.Failure,
      registerResetStatus: () => RequestStatus.Idle,
    },
  ],
  registerWeakPassword: [
    false,
    {
      setRegisterWeakPassword: (_, { weakPassword }) => weakPassword,
    },
  ],
  registerWrongEmail: [
    false,
    {
      setRegisterWrongEmail: (_, { wrongEmail }) => wrongEmail,
    },
  ],
  registerErrorDetail: [
    null as null | unknown,
    {
      registerFailure: (_, { errorDetail }) =>
        errorDetail !== undefined ? errorDetail : null,
    },
  ],
};
