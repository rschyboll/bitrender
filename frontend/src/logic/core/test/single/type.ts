import type { MakeOwnLogicType } from '@/logic/types';

interface Reducers {
  value: number;
}

interface Props {
  key: string;
}

export type SettingsLogicType = MakeOwnLogicType<{
  reducers: Reducers;
  props: Props;
}>;
