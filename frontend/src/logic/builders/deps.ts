/* eslint-disable @typescript-eslint/no-explicit-any */
import { interfaces } from "inversify";
import { LogicBuilder } from "kea";

import Dependencies from "@/deps";
import type { MakeOwnLogicType } from "@/logic/types/";
import { PartialRecord } from "@/types/utility";

type ReturnTypeOrNever<Type> = Type extends () => infer ReturnType
  ? ReturnType
  : never;

type DepsBuilderInput<Deps extends MakeOwnLogicType["deps"]> = {
  [Key in keyof Deps]:
    | interfaces.ServiceIdentifier<Deps[Key]>
    | {
        identifier: interfaces.ServiceIdentifier<ReturnTypeOrNever<Deps[Key]>>;
        named: true;
      };
};

export function deps<L extends MakeOwnLogicType>(
  input: DepsBuilderInput<L["deps"]>
): LogicBuilder<L> {
  return (logic) => {
    const dependencies: PartialRecord<
      keyof L["deps"],
      unknown | ((key: string) => unknown)
    > = {};
    for (const inputKey in input) {
      const dependency = input[inputKey];
      if (typeof dependency == "symbol") {
        const dependencyKey = dependency as interfaces.ServiceIdentifier;
        Object.defineProperty(dependencies, inputKey, {
          get: function () {
            return Dependencies.get(dependencyKey);
          },
        });
      } else {
        const dependencyObject = dependency as {
          identifier: interfaces.ServiceIdentifier;
        };
        dependencies[inputKey] = (key: string) =>
          Dependencies.getNamed(dependencyObject.identifier, key);
      }
    }
    logic.deps = dependencies;

    return logic;
  };
}
