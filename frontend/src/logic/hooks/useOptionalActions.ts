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

export function useOptionalActions<L extends Logic = Logic>(
  logic: BuiltLogic<L> | LogicWrapper<L>,
): Partial<L['actions']> {
  const builtLogicContext = isLogicWrapper(logic)
    ? getContext().react.contexts.get(logic)
    : null;
  const defaultBuiltLogic = useContext(builtLogicContext || blankContext);
  const builtLogic = isLogicWrapper(logic)
    ? defaultBuiltLogic || logic.build()
    : logic;

  const isMounted = useSelector(() => builtLogic.isMounted());

  return useMemo(() => {
    if (!isMounted) {
      return {};
    } else {
      return builtLogic.actions;
    }
  }, [builtLogic.pathString, isMounted]);
}
