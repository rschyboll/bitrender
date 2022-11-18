import { memo } from 'react';
import { Trans } from 'react-i18next';

import { RecordValueType } from '@/types/utility';

import { ColumnType } from '../enums';
import { ColumnTypeValues } from '../types/model';
import { BooleanColumn } from './boolean';
import styles from './style.module.scss';
import { TrueOrNullColumn } from './trueOrNull';

export type ColumnBodyProps = RecordValueType<{
  [Key in ColumnType]: {
    type: Key;
    value: ColumnTypeValues[Key];
  };
}>;

const ColumnBody = memo(function ColumnBody(props: ColumnBodyProps) {
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

interface ColumnHeaderProps {
  type: ColumnType;
  title: string;
}

const ColumnHeader = memo(function ColumnHeader(props: ColumnHeaderProps) {
  return (
    <div>
      <Trans>{props.title}</Trans>
    </div>
  );
});

export const Column = {
  Body: ColumnBody,
  Header: ColumnHeader,
  getHeaderClassName: (type: ColumnType) =>
    [ColumnType.BOOL, ColumnType.TRUEORNULL].includes(type)
      ? styles.iconHeader
      : styles.header,
  getCellClassName: (type: ColumnType) => styles.cell,
};
