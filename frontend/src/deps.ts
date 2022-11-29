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
import { bindLogicDependencies } from '@/logic/deps';
import { RoleService, UserService } from '@/services/api';
import { IRoleService, IUserService } from '@/services/interfaces';
import {
  RoleValidators,
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

const Dependencies = new Container();

bindLogicDependencies(Dependencies);

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

//Service dependencies
Dependencies.bind(IUserService.$).to(UserService).inSingletonScope();
Dependencies.bind(IRoleService.$).to(RoleService).inSingletonScope();

export default Dependencies;
