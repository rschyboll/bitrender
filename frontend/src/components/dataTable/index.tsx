import { interfaces } from 'inversify';
import { useInjection } from 'inversify-react';
import { Logic, LogicWrapper, useActions, useValues } from 'kea';
import {
  DataTableHeaderTemplateType,
  DataTablePFSEvent,
  DataTable as PrimeDataTable,
} from 'primereact/datatable';
import { memo, useCallback } from 'react';

import { PaginatorTemplate } from '@/components/paginator';

import './style.scss';

interface IDataTableLogicBase extends Logic {
  readonly actions: {
    setCurrentPage: (currentPage: number) => void;
    setRowsPerPage: (rowsPerPage: number) => void;
  };
  readonly values: {
    currentPage: number;
    rowsPerPage: number;
    amountOfRecords: number | null;
  };
}

export type IDataTableLogic = LogicWrapper<IDataTableLogicBase>;

export interface DataTableProps {
  logicIdentifier: interfaces.ServiceIdentifier<IDataTableLogic>;
  header?: DataTableHeaderTemplateType;
}

export const DataTable = memo(function DataTable(props: DataTableProps) {
  const dataTableLogic = useInjection(props.logicIdentifier);

  const { currentPage, rowsPerPage, amountOfRecords } =
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
    />
  );
});
