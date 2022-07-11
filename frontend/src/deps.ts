import { Container } from 'inversify';
import { useInjection } from 'inversify-react';

import { settingsLogic } from './logic/core/settings';
import { ISettingsLogic } from './logic/interfaces';

type DepTypes = {
  LOGIC: {
    SETTINGS: ISettingsLogic;
  };
};

const Deps = {
  LOGIC: {
    SETTINGS: Symbol.for('LOGIC/SETTINGS'),
  },
};

export const DepContainer = new Container();

DepContainer.bind<ISettingsLogic>(Deps.LOGIC.SETTINGS).toConstantValue(
  settingsLogic,
);

class Dependencies {
  public static use<
    Key extends keyof typeof Deps & keyof DepTypes,
    ID extends keyof typeof Deps[Key] & keyof DepTypes[Key],
  >(key: Key, id: ID): DepTypes[Key][ID] {
    return useInjection(Deps[key][id] as unknown as symbol);
  }

  public static get<
    Key extends keyof typeof Deps & keyof DepTypes,
    ID extends keyof typeof Deps[Key] & keyof DepTypes[Key],
  >(key: Key, id: ID): DepTypes[Key][ID] {
    return DepContainer.get(Deps[key][id] as unknown as symbol);
  }
}

export default Dependencies;

export { Dependencies };
