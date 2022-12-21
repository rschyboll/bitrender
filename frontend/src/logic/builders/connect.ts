import { ConnectDefinitions, LogicBuilder, connect as keaConnect } from 'kea';

import type { MakeOwnLogicType } from '@/logic/types/';

export function connect<Logic extends MakeOwnLogicType>(
  input: (logic: Logic) => ConnectDefinitions,
): LogicBuilder<Logic> {
  return (logic) => {
    const connectInput = typeof input === 'function' ? input(logic) : input;

    if (logic.path.includes('userCount')) {
      keaConnect(connectInput)(logic);
    } else {
      keaConnect(connectInput)(logic);
    }
    return logic;
  };
}
