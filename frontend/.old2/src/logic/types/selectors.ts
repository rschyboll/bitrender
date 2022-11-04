/* eslint-disable @typescript-eslint/no-explicit-any, @typescript-eslint/ban-types*/
import type { Logic } from 'kea';
import type { DefaultMemoizeOptions } from 'reselect';

import type { MakeOwnLogicType } from './makeLogic';

declare type LogicPropSelectors<LogicType extends Logic> = {
  [PK in keyof LogicType['props']]: () => LogicType['props'][PK];
};

type SelectorInputTuple<T extends any[]> = {
  [Key in keyof T]: (...args: any[]) => T[Key];
};

type SelectorDefinition<
  Selectors extends MakeOwnLogicType['selectors'],
  PropSelectors extends LogicPropSelectors<MakeOwnLogicType>,
  SelectorF extends (...args: any[]) => any,
> = SelectorF extends (...args: infer Args) => infer ReturnT
  ?
      | [
          (s: Selectors, p: PropSelectors) => SelectorInputTuple<Args>,
          (...args: Args) => ReturnT,
          DefaultMemoizeOptions,
        ]
      | [
          (s: Selectors, p: PropSelectors) => SelectorInputTuple<Args>,
          (...args: Args) => ReturnT,
        ]
  : never;

type SelectorDefinitions<LogicType extends MakeOwnLogicType> = {
  [Key in keyof LogicType['__internal_selector_types']]: LogicType['__internal_selector_types'][Key] extends (
    ...args: any[]
  ) => any
    ? SelectorDefinition<
        LogicType['selectors'],
        LogicPropSelectors<LogicType>,
        LogicType['__internal_selector_types'][Key]
      >
    : never;
};

export type SelectorsDef<Logic extends MakeOwnLogicType> =
  | ((logic: Logic) => SelectorDefinitions<Logic>)
  | SelectorDefinitions<Logic>;
