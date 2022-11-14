import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Button } from 'primereact/button';
import { Dialog } from 'primereact/dialog';
import { FC, useCallback, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { IoAdd } from 'react-icons/io5';
import { RiSearchLine } from 'react-icons/ri';

import { Card, IconCard } from '@/components/card';
import { DataTable } from '@/components/dataTable';
import { TextField } from '@/components/textField';
import { ICreateRoleLogic, IRolesTableLogic } from '@/logic/interfaces';
import { RequestStatus } from '@/services';

import { ModifyColumn } from './columns/modify';
import {
  CreateDialogFooter,
  CreateDialogIcons,
  CreateRoleDialog,
} from './dialogs';
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
        titleActions={
          <>
            <TableSearchField />
            <TableAddButton />
          </>
        }
        className="roles-table-card col-12"
      >
        <DataTable
          logicIdentifier={IRolesTableLogic.$}
          model={rolesTableModel}
          customColumns={{
            after: {
              modify: {
                content: ModifyColumn,
              },
            },
          }}
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
    <TextField
      value={searchString != null ? searchString : ''}
      onChange={setSearchString}
      className="search-field"
      leftIcon={RiSearchLine}
      hasFloor={false}
      placeholder={'search'}
    />
  );
};

const TableAddButton = () => {
  const { t } = useTranslation();
  const addRoleLogic = useInjection(ICreateRoleLogic.$);

  const [dialogVisible, setDialogVisible] = useState(false);

  const onAddNewButtonClick = useCallback(
    () => setDialogVisible(!dialogVisible),
    [dialogVisible],
  );

  const onDialogDismiss = useCallback(() => {
    if (
      addRoleLogic.isMounted() &&
      addRoleLogic.values.saveStatus == RequestStatus.Running
    ) {
      return;
    }
    return setDialogVisible(false);
  }, [addRoleLogic]);

  const onDialogClose = useCallback(() => setDialogVisible(false), []);

  return (
    <>
      <Button
        className="add-new-button"
        label={t('newFemale')}
        icon={<IoAdd size="1.75rem" />}
        onClick={onAddNewButtonClick}
      />
      <Dialog
        visible={dialogVisible}
        onHide={onDialogDismiss}
        icons={<CreateDialogIcons closeDialog={onDialogClose} />}
        dismissableMask
        closable={false}
        header={t('role.create')}
        footer={<CreateDialogFooter closeDialog={onDialogClose} />}
        style={{ minWidth: '35rem' }}
      >
        <CreateRoleDialog />
      </Dialog>
    </>
  );
};

export default RolesPage;
