/* eslint-disable react-hooks/exhaustive-deps */

/* eslint-disable react-hooks/rules-of-hooks */
import {
  BuiltLogic,
  Logic,
  LogicWrapper,
  getContext,
  isLogicWrapper,
  useSelector,
} from 'kea';
import { createContext, useContext, useMemo } from 'react';

const blankContext = createContext(undefined as BuiltLogic | undefined);

export function useOptionalValues<L extends Logic = Logic>(
  logic: BuiltLogic<L> | LogicWrapper<L>,
): Partial<L['values']> {
  const builtLogicContext = isLogicWrapper(logic)
    ? getContext().react.contexts.get(logic)
    : null;
  const defaultBuiltLogic = useContext(builtLogicContext || blankContext);
  const builtLogic = isLogicWrapper(logic)
    ? defaultBuiltLogic || logic.build()
    : logic;

  const isMounted = useSelector(() => builtLogic.isMounted());

  return useMemo(() => {
    const response = {};

    if (!isMounted) {
      for (const key of Object.keys(builtLogic.selectors)) {
        Object.defineProperty(response, key, {
          get: () => useSelector(() => undefined),
        });
      }
      return response;
    }

    for (const key of Object.keys(builtLogic.selectors)) {
      Object.defineProperty(response, key, {
        get: () => useSelector(builtLogic.selectors[key]),
      });
    }

    return response;
  }, [builtLogic.pathString, isMounted]);
}
