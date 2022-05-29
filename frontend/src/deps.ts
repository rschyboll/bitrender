import { Container } from 'inversify';
import { useInjection as useReactInjection } from 'inversify-react';

import { SettingsLogic } from './logic/interfaces/settings';
import { settingsLogic } from './logic/settings';

export const SERVICE = {
  SETTINGS_LOGIC: Symbol.for('Settings logic'),
};

const SERVICES = {
  [SERVICE.SETTINGS_LOGIC]: settingsLogic,
};

export const Dependencies = new Container();

Dependencies.bind<SettingsLogic>(SERVICE.SETTINGS_LOGIC).toConstantValue(
  settingsLogic,
);

const useInjection = <Key extends keyof typeof SERVICE>(
  id: Key,
): typeof SERVICES[typeof SERVICE[Key]] => {
  return Dependencies.get(id);
};

const test = useInjection('SETTINGS_LOGIC');
