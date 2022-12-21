/* eslint-disable @typescript-eslint/no-explicit-any */
import { interfaces } from 'inversify';
import { LogicBuilder, LogicWrapper, isLogicWrapper } from 'kea';

import Dependencies from '@/deps';
import type { MakeOwnLogicType } from '@/logic/types/';
import type { PartialRecord } from '@/types/utility';

type DepsBuilderInput<Deps extends MakeOwnLogicType['deps']> = {
  [Key in keyof Deps]:
    | interfaces.ServiceIdentifier<Deps[Key]>
    | {
        identifier: interfaces.ServiceIdentifier<Deps[Key]>;
        name: () => string;
      }
    | (Deps[Key] extends MakeOwnLogicType
        ? unknown extends Deps[Key]['props']
          ? never
          : {
              identifier: interfaces.ServiceIdentifier<Deps[Key]>;
              props: () => Deps[Key]['props'];
            }
        : never);
};

//Jeśli się zastanawiasz, dlaczego nie działa gdy używasz values jako props do kolejnej logiki
//i używasz jej w connect lub w innym miejscu, trafiłeś dobrze. Odpowiedź brzmi, nie da się,
//wymagałoby to forka całej Kei, tak naprawdę stworzenie biblioteki Rekea, ale myślałem o tym, nie polecam.
//Musisz znaleźć inny sposób.
export function deps<L extends MakeOwnLogicType>(
  input:
    | DepsBuilderInput<L['deps']>
    | ((props: L['props']) => DepsBuilderInput<L['deps']>),
): LogicBuilder<L> {
  return (logic) => {
    const dependencies: PartialRecord<
      keyof L['deps'],
      unknown | ((key: string) => unknown)
    > = {};
    const deps = typeof input === 'function' ? input(logic['props']) : input;

    for (const inputKey in deps) {
      let dependencyID = deps[inputKey];
      if (typeof dependencyID == 'symbol') {
        const dependencyKey = dependencyID as interfaces.ServiceIdentifier;
        Object.defineProperty(dependencies, inputKey, {
          get: function () {
            const dependency = Dependencies.get(dependencyKey);
            if (isLogicWrapper(dependency)) {
              return dependency();
            }
            return dependency;
          },
        });
      } else if ('props' in dependencyID) {
        const dependencyObject = dependencyID as {
          identifier: interfaces.ServiceIdentifier<
            LogicWrapper<MakeOwnLogicType>
          >;
          props: () => unknown;
        };
        Object.defineProperty(dependencies, inputKey, {
          get: function () {
            return Dependencies.get(dependencyObject.identifier)(
              dependencyObject.props(),
            );
          },
        });
      } else if ('name' in dependencyID) {
        const dependencyObject = dependencyID as {
          identifier: interfaces.ServiceIdentifier<
            LogicWrapper<MakeOwnLogicType>
          >;
          name: () => string;
        };
        Object.defineProperty(dependencies, inputKey, {
          get: function () {
            const dependency = Dependencies.getNamed(
              dependencyObject.identifier,
              dependencyObject.name(),
            );
            if (isLogicWrapper(dependency)) {
              return dependency();
            }
            return dependency;
          },
        });
      }
    }
    logic.deps = dependencies;

    return logic;
  };
}
