import type { MakeOwnLogicType } from '@/logic/types';

interface Reducers {
  value: number;
}

interface Props {
  key: string;
}

interface Actions {
  updateValue: true;
}

export type SettingsLogicType = MakeOwnLogicType<{
  reducers: Reducers;
  props: Props;
  actions: Actions;
}>;
