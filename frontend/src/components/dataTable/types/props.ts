import type { interfaces } from 'inversify';
import type {
  DataTableHeaderTemplateType,
  DataTableProps as PrimeDataTableProps,
} from 'primereact/datatable';
import type { FC } from 'react';

import type {
  ArrayElementType,
  ServiceTypeFromIdentifier,
} from '@/types/utility';

import type { IDataTableLogic } from './logic';
import type { DataTableModel } from './model';

type DataTableValueType<
  LogicIdentifier extends interfaces.ServiceIdentifier<IDataTableLogic>,
> = ServiceTypeFromIdentifier<LogicIdentifier> extends IDataTableLogic
  ? ArrayElementType<
      ServiceTypeFromIdentifier<LogicIdentifier>['values']['values']
    >
  : never;

type CustomColumn<
  LogicIdentifier extends interfaces.ServiceIdentifier<IDataTableLogic>,
> = {
  title?: string;
  content: FC<{
    value: ServiceTypeFromIdentifier<LogicIdentifier> extends IDataTableLogic
      ? ArrayElementType<
          ServiceTypeFromIdentifier<LogicIdentifier>['values']['values']
        >
      : never;
  }>;
};

export interface DataTableProps<
  LogicIdentifier extends interfaces.ServiceIdentifier<IDataTableLogic>,
> {
  logicIdentifier: LogicIdentifier;
  model: DataTableModel<DataTableValueType<LogicIdentifier>>;
  header?: DataTableHeaderTemplateType;
  customColumns?: {
    before?: Record<string, CustomColumn<LogicIdentifier>>;
    after?: Record<string, CustomColumn<LogicIdentifier>>;
  };
  selection?:
    | DataTableValueType<LogicIdentifier>
    | DataTableValueType<LogicIdentifier>[]
    | null;
  selectionMode?: PrimeDataTableProps['selectionMode'];
  onRowSelectionChange?: (
    value:
      | DataTableValueType<LogicIdentifier>
      | DataTableValueType<LogicIdentifier>[],
  ) => void;
}
