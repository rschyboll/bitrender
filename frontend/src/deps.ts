import { Container } from 'inversify';
import 'reflect-metadata';

import { UserConverters, UtilityConverters } from '@/converters/core';
import { IUserConverters, IUtilityConverters } from '@/converters/interfaces';
import {
  appLogic,
  authLogic,
  rolesTableLogic,
  routeLogic,
  settingsLogic,
} from '@/logic/core';
import {
  IAppLogic,
  IAuthLogic,
  IRolesTableLogic,
  IRouteLogic,
  ISettingsLogic,
} from '@/logic/interfaces';
import { UserService } from '@/services/api';
import { IUserService } from '@/services/interfaces';
import {
  RouteValidators,
  ServiceValidators,
  UserValidators,
} from '@/validators/core';
import {
  IRouteValidators,
  IServiceValidators,
  IUserValidators,
} from '@/validators/interfaces';

const Dependencies = new Container();

//Validator dependencies
Dependencies.bind(IUserValidators.$).to(UserValidators).inSingletonScope();
Dependencies.bind(IServiceValidators.$)
  .to(ServiceValidators)
  .inSingletonScope();
Dependencies.bind(IRouteValidators.$).to(RouteValidators).inSingletonScope();

//Converter dependencies
Dependencies.bind(IUserConverters.$).to(UserConverters).inSingletonScope();
Dependencies.bind(IUtilityConverters.$)
  .to(UtilityConverters)
  .inSingletonScope();

//Logic dependencies
Dependencies.bind(IAppLogic.$).toConstantValue(appLogic);
Dependencies.bind(ISettingsLogic.$).toConstantValue(settingsLogic);
Dependencies.bind(IAuthLogic.$).toConstantValue(authLogic);
Dependencies.bind(IRouteLogic.$).toConstantValue(routeLogic);
Dependencies.bind(IRolesTableLogic.$).toConstantValue(rolesTableLogic);

//Service dependencies
Dependencies.bind(IUserService.$).to(UserService).inSingletonScope();

export default Dependencies;
