import { interfaces } from 'inversify';
import { DataTableHeaderTemplateType } from 'primereact/datatable';
import { FC } from 'react';

import { ArrayElementType, ServiceTypeFromIdentifier } from '@/types/utility';

import { IDataTableLogic } from './logic';
import { DataTableModel } from './model';

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
  model: ServiceTypeFromIdentifier<LogicIdentifier> extends IDataTableLogic
    ? DataTableModel<
        ArrayElementType<
          ServiceTypeFromIdentifier<LogicIdentifier>['values']['values']
        >
      >
    : never;
  header?: DataTableHeaderTemplateType;
  customColumns?: {
    before?: Record<string, CustomColumn<LogicIdentifier>>;
    after?: Record<string, CustomColumn<LogicIdentifier>>;
  };
}
