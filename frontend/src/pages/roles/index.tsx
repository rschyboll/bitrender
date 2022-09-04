import { Card } from 'primereact/card';
import { FC } from 'react';
import { RiSearchLine } from 'react-icons/ri';

import { DataTable } from '@/components/dataTable';
import { TextField } from '@/components/textField';
import { IRolesTableLogic } from '@/logic/interfaces';

import './style.scss';

const RolesPage: FC = () => {
  return (
    <div className="roles-page">
      <Card className="roles-table-card">
        <DataTable logicIdentifier={IRolesTableLogic.$} />
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
