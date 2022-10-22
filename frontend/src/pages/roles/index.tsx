import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Button } from 'primereact/button';
import { FC, useCallback } from 'react';
import { RiSearchLine } from 'react-icons/ri';

import { Card, IconCard } from '@/components/card';
import { DataTable } from '@/components/dataTable';
import { TextField } from '@/components/textField';
import { IRolesTableLogic } from '@/logic/interfaces';

import './style.scss';
import { rolesTableModel } from './tableModel';

const RolesPage: FC = () => {
  return (
    <div className="roles-page grid">
      <IconCard
        className="roles-default-role-card col-12 desktop:col-6"
        title="Orders"
        color="#64B5F6"
        icon={RiSearchLine}
      >
        Test
      </IconCard>
      <IconCard
        className="roles-default-role-counter-card col-12 desktop:col-6"
        title="Orders"
        color="#64B5F6"
        icon={RiSearchLine}
      >
        Test
      </IconCard>
      <Card
        title="Lista roli użytkowników"
        titleActions={<TableSearchField />}
        className="roles-table-card col-12"
      >
        <DataTable
          model={rolesTableModel}
          logicIdentifier={IRolesTableLogic.$}
        />
      </Card>
    </div>
  );
};

const TableSearchField = () => {
  const rolesTableLogic = useInjection(IRolesTableLogic.$);

  const { searchString } = useValues(rolesTableLogic);
  const { setSearchString } = useActions(rolesTableLogic);

  return (
    <div className="roles-table-header">
      <TextField
        value={searchString != null ? searchString : ''}
        onChange={setSearchString}
        className="search-field"
        leftIcon={RiSearchLine}
        hasFloor={false}
        placeholder={'search'}
      />
    </div>
  );
};

export default RolesPage;
