import { Container } from 'inversify';
import 'reflect-metadata';

import {
  RoleConverters,
  UserConverters,
  UtilityConverters,
} from '@/converters/core';
import {
  IRoleConverters,
  IUserConverters,
  IUtilityConverters,
} from '@/converters/interfaces';
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
import { RoleService, UserService } from '@/services/api';
import { IRoleService, IUserService } from '@/services/interfaces';
import {
  RouteValidators,
  ServiceValidators,
  UserValidators,
} from '@/validators/core';
import {
  IRoleValidators,
  IRouteValidators,
  IServiceValidators,
  IUserValidators,
} from '@/validators/interfaces';

import { RoleValidators } from './validators/core/role';

const Dependencies = new Container();

//Validator dependencies
Dependencies.bind(IUserValidators.$).to(UserValidators).inSingletonScope();
Dependencies.bind(IServiceValidators.$)
  .to(ServiceValidators)
  .inSingletonScope();
Dependencies.bind(IRouteValidators.$).to(RouteValidators).inSingletonScope();
Dependencies.bind(IRoleValidators.$).to(RoleValidators).inSingletonScope();

//Converter dependencies
Dependencies.bind(IUserConverters.$).to(UserConverters).inSingletonScope();
Dependencies.bind(IUtilityConverters.$)
  .to(UtilityConverters)
  .inSingletonScope();
Dependencies.bind(IRoleConverters.$).to(RoleConverters).inSingletonScope();

//Logic dependencies
Dependencies.bind(IAppLogic.$).toConstantValue(appLogic);
Dependencies.bind(ISettingsLogic.$).toConstantValue(settingsLogic);
Dependencies.bind(IAuthLogic.$).toConstantValue(authLogic);
Dependencies.bind(IRouteLogic.$).toConstantValue(routeLogic);
Dependencies.bind(IRolesTableLogic.$).toConstantValue(rolesTableLogic);

//Service dependencies
Dependencies.bind(IUserService.$).to(UserService).inSingletonScope();
Dependencies.bind(IRoleService.$).to(RoleService).inSingletonScope();

export default Dependencies;
