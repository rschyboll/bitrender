import type { Container } from 'inversify';

import * as Core from './core';
import * as Interfaces from './interfaces';

export function bindLogicDependencies(Dependencies: Container) {
  Dependencies.bind(Interfaces.IAppLogic.$).toConstantValue(Core.appLogic);
  Dependencies.bind(Interfaces.IAuthLogic.$).toConstantValue(Core.authLogic);
  Dependencies.bind(Interfaces.IRouteLogic.$).toConstantValue(Core.routeLogic);
  Dependencies.bind(Interfaces.ISettingsLogic.$).toConstantValue(
    Core.settingsLogic,
  );

  //ROLES
  Dependencies.bind(Interfaces.IRoleTableLoaderLogic.$).toConstantValue(
    Core.rolesTableLoaderLogic,
  );
  Dependencies.bind(Interfaces.IRoleTableLogic.$).toConstantValue(
    Core.rolesTableLogic,
  );
  Dependencies.bind(Interfaces.IRoleCreateLogic.$).toConstantValue(
    Core.roleCreateLogic,
  );
}
