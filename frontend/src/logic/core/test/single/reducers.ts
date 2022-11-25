import type { ReducersDef } from '@/logic';

import type { SettingsLogicType } from './type';

let counter = 0;

const getDefaultValue = () => {
  counter++;
  return counter;
};

export const Reducers: ReducersDef<SettingsLogicType> = () => ({
  value: [getDefaultValue(), { updateValue: (state) => state + 1 }],
});
