import { Card } from 'primereact/card';
import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { FC } from 'react';
import { RiSearchLine } from 'react-icons/ri';

import { TextField } from '@/components/textField';

import './style.scss';

const RolesPage: FC = () => {
  return (
    <div className="roles-page">
      <Card className="roles-table-card">
        <DataTable className="roles-table" header={<RolesPageTableHeader />}>
          <Column />
        </DataTable>
      </Card>
    </div>
  );
};

const RolesPageTableHeader = () => {
  return (
    <div className="roles-table-header">
      <span className="roles-table-title">Test</span>
      <TextField
        value=""
        onChange={() => {}}
        className="search-field"
        leftIcon={RiSearchLine}
        hasFloor={false}
        placeholder={'search'}
      />
    </div>
  );
};

export default RolesPage;
