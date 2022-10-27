import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { after } from 'lodash';
import { Button } from 'primereact/button';
import { FC } from 'react';
import { useTranslation } from 'react-i18next';
import { IoAdd } from 'react-icons/io5';
import { RiSearchLine } from 'react-icons/ri';

import { Card, IconCard } from '@/components/card';
import { DataTable } from '@/components/dataTable';
import { TextField } from '@/components/textField';
import { IRolesTableLogic } from '@/logic/interfaces';

import { ModifyColumn } from './columns/modify';
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
          logicIdentifier={IRolesTableLogic.$}
          model={rolesTableModel}
          customColumns={{
            after: {
              modify: ModifyColumn,
            },
          }}
        />
      </Card>
    </div>
  );
};

const TableSearchField = () => {
  const rolesTableLogic = useInjection(IRolesTableLogic.$);
  const { t } = useTranslation();

  const { searchString } = useValues(rolesTableLogic);
  const { setSearchString } = useActions(rolesTableLogic);

  return (
    <div className="roles-table-header">
      <Button
        className="add-new-button"
        label={t('new_female')}
        icon={<IoAdd size="1.75rem" />}
      />

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
