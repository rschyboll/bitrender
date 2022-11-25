/* eslint-disable @typescript-eslint/no-explicit-any, @typescript-eslint/ban-types*/
import { makeSelector } from '@taskworld.com/rereselect';
import { LogicBuilder, getContext } from 'kea';
import { DefaultMemoizeOptions, createSelector } from 'reselect';

import { MakeOwnLogicType } from '@/logic/types';
import { ArrayElementType, RestrictedObject } from '@/types/utility';

export type ReselectorsDefinitions<
  Logic extends MakeOwnLogicType & MakeReselectorsBuilderLogicType,
> = {
  [Key in keyof Logic['__internal_reselector_types']]:
    | [
        (
          selectors: Logic['selectors'],
        ) => (
          state: any,
          props?: any,
        ) => Parameters<Logic['__internal_reselector_types'][Key]>[0][],
        (
          value: Parameters<Logic['__internal_reselector_types'][Key]>[0],
        ) => (
          state: any,
          props?: any,
        ) => ArrayElementType<
          ReturnType<Logic['__internal_reselector_types'][Key]>
        >,
        DefaultMemoizeOptions,
      ]
    | [
        (
          selectors: Logic['selectors'],
        ) => (
          state: any,
          props?: any,
        ) => Parameters<Logic['__internal_reselector_types'][Key]>[0][],
        (
          value: Parameters<Logic['__internal_reselector_types'][Key]>[0],
        ) => (
          state: any,
          props?: any,
        ) => ArrayElementType<
          ReturnType<Logic['__internal_reselector_types'][Key]>
        >,
      ];
};

export type MakeReselectorsBuilderLogicType<
  Reselectors extends RestrictedObject<
    Reselectors,
    (value: any) => any[]
  > = RestrictedObject<any, (...args: any[]) => any[]>,
> = {
  selectors: {
    [Key in keyof Reselectors]: Reselectors[Key] extends (...args: any[]) => any
      ? (state: any, props: any) => ReturnType<Reselectors[Key]>
      : never;
  };
  values: {
    [Key in keyof Reselectors]: Reselectors[Key] extends (...args: any[]) => any
      ? ReturnType<Reselectors[Key]>
      : never;
  };
  __internal_reselector_types: Reselectors;
};

function checkLogicForExistingSelectors(
  logic: MakeOwnLogicType,
  selectorKeys: string[],
) {
  for (const key of selectorKeys) {
    console.log(logic.selectors[key]);
    if (typeof logic.selectors[key] !== 'undefined') {
      throw new Error(
        `[KEA] Logic "${logic.pathString}" selector "${key}" already exists`,
      );
    }
  }
}

export function reselectors<
  Logic extends MakeOwnLogicType & MakeReselectorsBuilderLogicType,
>(
  input:
    | ReselectorsDefinitions<Logic>
    | ((logic: Logic) => ReselectorsDefinitions<Logic>),
): LogicBuilder<Logic> {
  return (logic) => {
    const reselectorInputs = typeof input === 'function' ? input(logic) : input;
    checkLogicForExistingSelectors(logic, Object.keys(reselectorInputs));

    for (const key in reselectorInputs) {
      const reselector = reselectorInputs[key];
      const [input, outputSelectorFactory, memoizeOptions] = reselector;
      const inputSelector = input(logic.selectors);
      const selector = createSelector(
        [
          makeSelector((query) => {
            const inputData = query(inputSelector);
            const outputData = [];

            for (const value of inputData) {
              const outputValue = query(outputSelectorFactory(value));
              outputData.push(outputValue);
            }
            return outputData;
          }),
        ],
        (arg: any) => {
          return arg;
        },
        { memoizeOptions },
      );
      logic.selectors[key] = selector;
      Object.defineProperty(logic.values, key, {
        get: function () {
          return logic.selectors[key](
            getContext().store.getState(),
            logic.props,
          );
        },
      });
    }
  };
}
