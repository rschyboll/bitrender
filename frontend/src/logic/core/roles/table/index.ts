import { actions, kea, listeners, path, props, reducers } from 'kea';
import { urlToAction } from 'kea-router';

import Dependencies from '@/deps';
import { IRouteLogic } from '@/logic/interfaces/route';
import { injectDepsToLogic } from '@/logic/utils';
import { IUserService } from '@/services/interfaces';
import { RequestStatus, ServiceErrorType } from '@/types/service';
import { sleep } from '@/utils/async';
import { IUserValidators } from '@/validators/interfaces';

import { ApiErrorCodes } from '../../../../types/service';
import type { logicType } from './indexType';

const logic = kea<logicType>([
  path(['roles', 'table']),
  props({} as {}),
  actions({}),
  reducers({}),
  listeners(({ props, actions, values }) => ({})),
]);

export const rolesTableLogic = injectDepsToLogic(logic, () => ({}));
