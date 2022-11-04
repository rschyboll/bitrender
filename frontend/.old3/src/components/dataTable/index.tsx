import { interfaces } from 'inversify';
import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Column as PrimeColumn } from 'primereact/column';
import {
  DataTablePFSEvent,
  DataTable as PrimeDataTable,
} from 'primereact/datatable';
import { useCallback } from 'react';
import { useTranslation } from 'react-i18next';

import { PaginatorTemplate } from '@/components/paginator';
import { IRolesTableLogic } from '@/logic/interfaces';
import { typedMemo } from '@/utils/react';

import { Column } from './columns';
import { ColumnType } from './enums';
import './style.scss';
import type { IDataTableLogic } from './types/logic';
import type { DataTableProps } from './types/props';

export * from './types';
export * from './enums';

export const DataTable = typedMemo(function DataTable<
  LogicIdentifier extends interfaces.ServiceIdentifier<IDataTableLogic>,
>(props: DataTableProps<LogicIdentifier>) {
  const dataTableLogic = useInjection(props.logicIdentifier);
  const { t } = useTranslation();

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
      loading={false}
      className="datatable"
      paginator
      paginatorTemplate={PaginatorTemplate}
      value={values}
    >
      {props.customColumns != null && props.customColumns.before != null
        ? Object.entries(props.customColumns.before).map(([key, column]) => {
            return <PrimeColumn key={key} header={column.title} />;
          })
        : null}
      {Object.entries(props.model.columns).map(([key, column]) => {
        return (
          <PrimeColumn
            key={key}
            field={key}
            header={t(column.title)}
            className={
              column.type == ColumnType.TRUEORNULL ? 'text-center' : ''
            }
            headerClassName={
              column.type == ColumnType.TRUEORNULL ? 'text-center' : ''
            }
            body={(rowData) => {
              return <Column type={column.type} value={rowData[key]} />;
            }}
          />
        );
      })}
      {props.customColumns != null && props.customColumns.after != null
        ? Object.entries(props.customColumns.after).map(([key, column]) => {
            return <PrimeColumn key={key} header={column.title} />;
          })
        : null}
    </PrimeDataTable>
  );
});
