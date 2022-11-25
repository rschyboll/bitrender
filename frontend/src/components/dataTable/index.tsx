import { interfaces } from 'inversify';
import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Column as PrimeColumn } from 'primereact/column';
import {
  DataTablePFSEvent,
  DataTable as PrimeDataTable,
  DataTableSelectionChangeParams as PrimeDataTableSelectionChangeParams,
} from 'primereact/datatable';
import { useCallback, useLayoutEffect, useState } from 'react';

import { PaginatorTemplate } from '@/components/paginator';
import config from '@/config';
import { useWindowSize } from '@/hooks';
import { typedMemo } from '@/utils/react';

import { Column } from './columns';
import './style.scss';
import { ColumnDefinition } from './types';
import type { IDataTableLogic } from './types/logic';
import type { DataTableProps } from './types/props';

export * from './types';
export * from './enums';

export const DataTable = typedMemo(function DataTable<
  LogicIdentifier extends interfaces.ServiceIdentifier<IDataTableLogic>,
>(props: DataTableProps<LogicIdentifier>) {
  const { onRowSelectionChange } = props;
  const dataTableLogic = useInjection(props.logicIdentifier);

  const { currentPage, rowsPerPage, amountOfRecords, values } =
    useValues(dataTableLogic);
  const { setCurrentPage, setRowsPerPage } = useActions(dataTableLogic);
  const [componentRendered, setComponentRendered] = useState(false);

  const windowSize = useWindowSize();

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

  const onSelectionChange = useCallback(
    (e: PrimeDataTableSelectionChangeParams) => {
      if (e.type == 'row' && onRowSelectionChange != null) {
        onRowSelectionChange(e.value);
      }
    },
    [onRowSelectionChange],
  );

  useLayoutEffect(() => {
    setTimeout(() => {
      setComponentRendered(true);
    }, 0);
  }, []);

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
      selection={props.selection}
      selectionMode={props.selectionMode}
      onSelectionChange={onSelectionChange}
      breakpoint={config.cssBreakpoints.mobile}
      responsiveLayout="stack"
      scrollable={
        windowSize.width != null &&
        windowSize.width > config.breakpoints.mobile &&
        componentRendered
          ? true
          : false
      }
    >
      {props.customColumns != null && props.customColumns.before != null
        ? Object.entries(props.customColumns.before).map(([key, column]) => {
            return <PrimeColumn key={key} header={column.title} />;
          })
        : null}
      {Object.entries(props.model.columns).map(
        ([key, column]: [string, ColumnDefinition]) => {
          return (
            <PrimeColumn
              key={key}
              field={key}
              frozen={column.frozen}
              className={Column.getCellClassName(column.type)}
              header={<Column.Header type={column.type} title={column.title} />}
              headerClassName={Column.getHeaderClassName(column.type)}
              body={(rowData) => {
                return <Column.Body type={column.type} value={rowData[key]} />;
              }}
            />
          );
        },
      )}
      {props.customColumns != null && props.customColumns.after != null
        ? Object.entries(props.customColumns.after).map(([key, column]) => {
            return <PrimeColumn key={key} header={column.title} />;
          })
        : null}
    </PrimeDataTable>
  );
});
