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
import { ParametricSelector, createSelector } from 'reselect';

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
