import { interfaces } from 'inversify';
import { useInjection } from 'inversify-react';
import { Logic, LogicWrapper, useActions, useValues } from 'kea';
import { Column as PrimeColumn } from 'primereact/column';
import {
  DataTableHeaderTemplateType,
  DataTablePFSEvent,
  DataTable as PrimeDataTable,
} from 'primereact/datatable';
import { memo, useCallback } from 'react';
import { useTranslation } from 'react-i18next';

import { PaginatorTemplate } from '@/components/paginator';

import { StringColumn } from './columns';
import { ColumnType, DataTableModel } from './model';
import './style.scss';

export { DataTableModel };

interface IDataTableLogicBase extends Logic {
  readonly actions: {
    setCurrentPage: (currentPage: number) => void;
    setRowsPerPage: (rowsPerPage: number) => void;
  };
  readonly values: {
    currentPage: number;
    rowsPerPage: number;
    amountOfRecords: number | null;
    values: unknown[];
  };
}

export type IDataTableLogic = LogicWrapper<IDataTableLogicBase>;

export interface DataTableProps {
  logicIdentifier: interfaces.ServiceIdentifier<IDataTableLogic>;
  model: DataTableModel;
  header?: DataTableHeaderTemplateType;
}

export const DataTable = memo(function DataTable(props: DataTableProps) {
  const dataTableLogic = useInjection(props.logicIdentifier);

  const { currentPage, rowsPerPage, amountOfRecords, values } =
    useValues(dataTableLogic);
  const { setCurrentPage, setRowsPerPage } = useActions(dataTableLogic);

  const onPage = useCallback(
    (e: DataTablePFSEvent) => {
      if (e.page != null && e.page != currentPage) {
        setCurrentPage(e.page);
      }
      if (e.rows != null && e.rows != rowsPerPage) {
        setRowsPerPage(e.rows);
      }
    },
    [setCurrentPage, currentPage, setRowsPerPage, rowsPerPage],
  );

  return (
    <PrimeDataTable
      header={props.header}
      rows={rowsPerPage}
      totalRecords={amountOfRecords != null ? amountOfRecords : undefined}
      first={currentPage * rowsPerPage}
      onPage={onPage}
      lazy
      className="datatable"
      paginator
      paginatorTemplate={PaginatorTemplate}
      value={values}
    >
      {Object.entries(props.model.columns).map(([key, column]) => {
        return (
          <DataTableColumn key={key} title={column.title} type={column.type} />
        );
      })}
    </PrimeDataTable>
  );
});

interface DataTableColumnProps {
  key: string;
  title: string;
  type: ColumnType;
}

const DataTableColumn = (props: DataTableColumnProps) => {
  const { t } = useTranslation();

  switch (props.type) {
    case ColumnType.STRING:
      return <StringColumn key={props.key} title={props.title} />;

    default:
      return <PrimeColumn key={props.key} header={t(props.title)} />;
  }
};
