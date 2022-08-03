import { Container } from 'inversify';
import 'reflect-metadata';

import { appLogic, loginLogic, routeLogic, settingsLogic } from '@/logic/core';
import { IAppLogic, ILoginLogic, ISettingsLogic } from '@/logic/interfaces';
import { UserService } from '@/services/api';
import { IUserService } from '@/services/interfaces';
import { ServiceValidators, UserValidators } from '@/validators/core';
import { IServiceValidators, IUserValidators } from '@/validators/interfaces';

import { UserConverters, UtilityConverters } from './converters/core';
import { IUserConverters, IUtilityConverters } from './converters/interfaces';
import { IRouteLogic } from './logic/interfaces/route';

const Dependencies = new Container();

//Validator dependencies
Dependencies.bind(IUserValidators.$).to(UserValidators).inSingletonScope();
Dependencies.bind(IServiceValidators.$)
  .to(ServiceValidators)
  .inSingletonScope();

//Converter dependencies
Dependencies.bind(IUserConverters.$).to(UserConverters).inSingletonScope();
Dependencies.bind(IUtilityConverters.$)
  .to(UtilityConverters)
  .inSingletonScope();

//Logic dependencies
Dependencies.bind(IAppLogic.$).toConstantValue(appLogic);
Dependencies.bind(ISettingsLogic.$).toConstantValue(settingsLogic);
Dependencies.bind(ILoginLogic.$).toConstantValue(loginLogic);
Dependencies.bind(IRouteLogic.$).toConstantValue(routeLogic);

//Service dependencies
Dependencies.bind(IUserService.$).to(UserService).inSingletonScope();

export default Dependencies;
