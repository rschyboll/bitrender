import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Button } from 'primereact/button';
import { FC, useCallback, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { IoAdd } from 'react-icons/io5';
import { RiDeleteBin6Line, RiEdit2Fill, RiSearchLine } from 'react-icons/ri';

import { Card, IconCard } from '@/components/card';
import { DataTable } from '@/components/dataTable';
import { TextField } from '@/components/textField';
import { ICreateRoleLogic, IRolesTableLogic } from '@/logic/interfaces';
import { MRole } from '@/types/models';

import { EditRoleDialog } from './dialogs/edit2';
import './style.scss';
import { rolesTableModel } from './tableModel';

const RolesPage: FC = () => {
  const [selectedRole, setSelectedRole] = useState<MRole.TableView | null>(
    null,
  );

  const onRoleSelect = useCallback(
    (value: MRole.TableView | MRole.TableView[]) => {
      if (!Array.isArray(value)) {
        setSelectedRole(value);
      }
    },
    [],
  );

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
            <TableModifyButton selectedRole={selectedRole} />
            <TableDeleteButton selectedRole={selectedRole} />
          </>
        }
        className="roles-table-card col-12"
      >
        <DataTable
          logicIdentifier={IRolesTableLogic.$}
          model={rolesTableModel}
          onRowSelectionChange={onRoleSelect}
          selectionMode="single"
          selection={selectedRole}
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

  const [dialogVisible, setDialogVisible] = useState(false);

  const onClick = useCallback(
    () => setDialogVisible(!dialogVisible),
    [dialogVisible],
  );

  return (
    <>
      <Button
        className="add-new-button p-button-success"
        label={t('newFemale')}
        icon={<IoAdd size="1.75rem" />}
        onClick={onClick}
        tooltip={t('role.addButtonTooltip')}
        tooltipOptions={{ showDelay: 1000, position: 'top' }}
      />
      <EditRoleDialog
        logicIdentifier={ICreateRoleLogic.$}
        visible={dialogVisible}
        setVisible={setDialogVisible}
        title="role.create"
        acceptLabel={'create'}
      />
    </>
  );
};

interface TableModifyButtonProps {
  selectedRole: null | MRole.TableView;
}

const TableModifyButton = (props: TableModifyButtonProps) => {
  const { t } = useTranslation();

  const [dialogVisible, setDialogVisible] = useState(false);

  const onClick = useCallback(() => {
    setDialogVisible(true);
  }, []);

  return (
    <>
      <Button
        disabled={props.selectedRole == null}
        className="modify-button"
        label={t('modify')}
        icon={<RiEdit2Fill size="1.5rem" />}
        onClick={onClick}
        tooltip={t('role.modifyButtonTooltip')}
        tooltipOptions={{ showDelay: 1000, position: 'top' }}
      />
      {props.selectedRole != null ? (
        <EditRoleDialog
          logicIdentifier={ICreateRoleLogic.$}
          visible={dialogVisible}
          setVisible={setDialogVisible}
          title={`${t('role.edit')} ${props.selectedRole.name}`}
          acceptLabel={'modify'}
        />
      ) : null}
    </>
  );
};

interface TableDeleteButtonProps {
  selectedRole: null | MRole.TableView;
}

const TableDeleteButton = (props: TableDeleteButtonProps) => {
  const { t } = useTranslation();

  const [dialogVisible, setDialogVisible] = useState(false);

  const onClick = useCallback(() => {
    setDialogVisible(true);
  }, []);

  return (
    <>
      <Button
        disabled={props.selectedRole == null}
        className="delete-button p-button-danger"
        label={t('delete')}
        icon={<RiDeleteBin6Line size="1.4rem" />}
        onClick={onClick}
        tooltip={t('role.deleteButtonTooltip')}
        tooltipOptions={{ showDelay: 1000, position: 'top' }}
      />
      {props.selectedRole != null ? (
        <EditRoleDialog
          logicIdentifier={ICreateRoleLogic.$}
          visible={dialogVisible}
          setVisible={setDialogVisible}
          title={`${t('role.edit')} ${props.selectedRole.name}`}
          acceptLabel={'modify'}
        />
      ) : null}
    </>
  );
};

export default RolesPage;
