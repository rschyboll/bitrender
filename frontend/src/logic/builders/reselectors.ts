/* eslint-disable @typescript-eslint/no-explicit-any, @typescript-eslint/ban-types*/
import { makeSelector } from '@taskworld.com/rereselect';
import {
  Logic,
  LogicBuilder,
  LogicPropSelectors,
  Selector,
  SelectorDefinition,
  SelectorDefinitions,
  getContext,
} from 'kea';
import {
  DefaultMemoizeOptions,
  ParametricSelector,
  createSelector,
} from 'reselect';

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
          props: any,
        ) => Parameters<Logic['__internal_reselector_types'][Key]>[0][],
        (
          value: Parameters<Logic['__internal_reselector_types'][Key]>[0],
        ) => (
          state: any,
          props: any,
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
          props: any,
        ) => Parameters<Logic['__internal_reselector_types'][Key]>[0][],
        (
          value: Parameters<Logic['__internal_reselector_types'][Key]>[0],
        ) => (
          state: any,
          props: any,
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
  for (const key in selectorKeys) {
    if (typeof logic.selectors[key] !== undefined) {
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
      const [input, outputSelectorFactory] = reselector;

      const inputSelectors = input(logic.selectors);
      const selector = (state = getContext().store.getState()) => {
        console.log('TEST');
      };
    }
  };
}

export function selectors<L extends Logic = Logic>(
  input: SelectorDefinitions<L> | ((logic: L) => SelectorDefinitions<L>),
): LogicBuilder<L> {
  return (logic) => {
    const selectorInputs = typeof input === 'function' ? input(logic) : input;

    const builtSelectors: Record<string, Selector> = {};
    for (const key of Object.keys(selectorInputs)) {
      if (typeof logic.selectors[key] !== 'undefined') {
        throw new Error(
          `[KEA] Logic "${logic.pathString}" selector "${key}" already exists`,
        );
      }
      addSelectorAndValue(logic, key, (...args) =>
        builtSelectors[key](...args),
      );
    }

    const propSelectors =
      typeof Proxy !== 'undefined'
        ? new Proxy(logic.props, {
            get(target, prop) {
              if (!(prop in target)) {
                throw new Error(
                  `[KEA] Prop "${String(prop)}" not found for logic "${
                    logic.pathString
                  }". Attempted to use in a selector. Please specify a default via props({ ${String(
                    prop,
                  )}: '' }) to resolve.`,
                );
              }
              return () => target[prop];
            },
          })
        : (Object.fromEntries(
            Object.keys(logic.props).map((key) => [
              key,
              () => logic.props[key],
            ]),
          ) as LogicPropSelectors<L>);

    for (const entry of Object.entries(selectorInputs)) {
      const [key, [input, func, memoizeOptions]]: [
        string,
        SelectorDefinition<L['selectors'], LogicPropSelectors<L>, any>,
      ] = entry as any;
      const args: ParametricSelector<any, any, any>[] = input(
        logic.selectors,
        propSelectors,
      );

      if (args.filter((a) => typeof a !== 'function').length > 0) {
        const argTypes = args.map((a) => typeof a).join(', ');
        const msg = `[KEA] Logic "${logic.pathString}", selector "${key}" has incorrect input: [${argTypes}].`;
        throw new Error(msg);
      }
      builtSelectors[key] = createSelector(args, func, { memoizeOptions });

      addSelectorAndValue(
        logic,
        key,
        (state = getContext().store.getState(), props = logic.props) =>
          builtSelectors[key](state, props),
      );

      if (!logic.values.hasOwnProperty(key)) {
        Object.defineProperty(logic.values, key, {
          get: function () {
            return logic.selectors[key](
              getContext().store.getState(),
              logic.props,
            );
          },
          enumerable: true,
        });
      }
    }
  };
}

export function addSelectorAndValue<L extends Logic = Logic>(
  logic: L,
  key: string,
  selector: Selector,
): void {
  logic.selectors[key] = selector;
  if (!logic.values.hasOwnProperty(key)) {
    Object.defineProperty(logic.values, key, {
      get: function () {
        return logic.selectors[key](getContext().store.getState(), logic.props);
      },
      enumerable: true,
    });
  }
}
