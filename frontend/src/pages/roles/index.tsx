import { Localized } from '@fluent/react';
import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Button } from 'primereact/button';
import { FC, useCallback, useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { IoAdd } from 'react-icons/io5';
import { RiDeleteBin6Line, RiEdit2Fill, RiSearchLine } from 'react-icons/ri';

import { Card, IconCard } from '@/components/card';
import { DataTable } from '@/components/dataTable';
import { TextField } from '@/components/textField';
import {
  IRoleCreateLogic,
  IRoleTableLogic,
  IRoleUpdateLogic,
} from '@/logic/interfaces';
import { MRole } from '@/types/models';

import { DeleteRoleDialog } from './dialogs/delete';
import { EditRoleDialog } from './dialogs/edit';
import './style.scss';
import { rolesTableModel } from './tableModel';
import './translations';

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
    [setSelectedRole],
  );

  return (
    <div className="roles-page grid">
      <Card
        title="Lista roli użytkowników"
        titleActions={
          <>
            <div className="role-table-search">
              <TableSearchField />
            </div>
            <div className="role-table-actions">
              <TableAddButton />
              <TableModifyButton selectedRole={selectedRole} />
              <TableDeleteButton selectedRole={selectedRole} />
            </div>
          </>
        }
        className="roles-table-card col-12"
      >
        <DataTable
          logicIdentifier={IRoleTableLogic.$}
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
  const rolesTableLogic = useInjection(IRoleTableLogic.$);

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
  const roleCreateLogic = useInjection(IRoleCreateLogic.$);

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
        logic={roleCreateLogic}
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
  const roleUpdateLogic = useInjection(IRoleUpdateLogic.$);

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
          logic={roleUpdateLogic({ id: props.selectedRole.id })}
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
        <DeleteRoleDialog
          id={props.selectedRole.id}
          visible={dialogVisible}
          setVisible={setDialogVisible}
        />
      ) : null}
    </>
  );
};

export default RolesPage;
