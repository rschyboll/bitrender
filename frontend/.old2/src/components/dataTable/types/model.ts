import { KeysMatching } from '@/types/utility';

import { ColumnType } from '../enums';

export interface ColumnTypeValues {
  [ColumnType.NUMBER]: number;
  [ColumnType.STRING]: string;
  [ColumnType.BOOL]: boolean;
  [ColumnType.TRUEORNULL]: true | null;
  [ColumnType.TAG]: {
    text: string;
    color: string;
  };
  [ColumnType.DATE]: Date;
}

export interface ColumnDefinition<Type extends ColumnType> {
  title: string;
  type: Type;
  sortable?: boolean;
  filterable?: boolean;
}

export interface DataTableModel<Values extends Record<string, unknown>> {
  columns: {
    [Key in keyof Values]: ColumnDefinition<
      KeysMatching<ColumnTypeValues, Values[Key]>
    >;
  };
}
