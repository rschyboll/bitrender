import { FC } from 'react';
import { RiSearchLine } from 'react-icons/ri';

import { Card, IconCard } from '@/components/card';
import { DataTable } from '@/components/dataTable';
import { TextField } from '@/components/textField';
import { IRolesTableLogic } from '@/logic/interfaces';

import './style.scss';

const RolesPage: FC = () => {
  return (
    <div className="roles-page">
      <IconCard
        className="roles-default-role-card"
        title="Orders"
        color="#64B5F6"
        icon={RiSearchLine}
      >
        Test
      </IconCard>
      <Card className="roles-table-card">
        <DataTable
          header={RolesPageTableHeader}
          logicIdentifier={IRolesTableLogic.$}
        />
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
