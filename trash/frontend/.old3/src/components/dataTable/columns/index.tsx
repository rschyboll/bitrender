import { memo } from 'react';

import { RecordValueType } from '@/types/utility';

import { ColumnType } from '../enums';
import { ColumnTypeValues } from '../types/model';
import { BooleanColumn } from './boolean';
import { TrueOrNullColumn } from './trueOrNull';

export type ColumnProps = RecordValueType<{
  [Key in ColumnType]: {
    type: Key;
    value: ColumnTypeValues[Key];
  };
}>;

export const Column = memo(function Column(props: ColumnProps) {
  switch (props.type) {
    case ColumnType.STRING:
      return <span>{props.value}</span>;
    case ColumnType.BOOL:
      return <BooleanColumn value={props.value} />;
    case ColumnType.TRUEORNULL:
      return <TrueOrNullColumn value={props.value} />;

    default:
      return <span>{props.value?.toString()}</span>;
  }
});
