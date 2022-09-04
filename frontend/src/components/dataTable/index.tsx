import { interfaces } from 'inversify';
import { useInjection } from 'inversify-react';
import { Logic, LogicWrapper } from 'kea';
import { DataTable as PrimeDataTable } from 'primereact/datatable';
import { memo } from 'react';

import { PaginatorTemplate } from '@/components/paginator';

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
}

export const DataTable = memo(function DataTable(props: DataTableProps) {
  const dataTableLogic = useInjection(props.logicIdentifier);

  return (
    <PrimeDataTable
      className="datatable"
      paginator
      paginatorTemplate={PaginatorTemplate}
    />
  );
});
