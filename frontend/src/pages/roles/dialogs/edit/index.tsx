import { interfaces } from 'inversify';
import { useInjection } from 'inversify-react';
import { LogicWrapper, useActions, useValues } from 'kea';
import { memo, useCallback } from 'react';
import { Trans } from 'react-i18next';

import { Checkbox } from '@/components/checkbox';
import { Dialog } from '@/components/dialog';
import { TextField } from '@/components/textField';
import { MakeOwnLogicType } from '@/logic';
import { useOptionalActions, useOptionalValues } from '@/logic/hooks';
import { RequestStatus } from '@/services';
import { MRole } from '@/types/models';
import { IRoleValidators } from '@/validators/interfaces';

import styles from './style.module.scss';

type EditRoleLogic = LogicWrapper<
  MakeOwnLogicType<{
    values: {
      name: string;
      selectedPermissions: Set<MRole.Permission>;
      isDefault: boolean | null;
      saveStatus: RequestStatus;
      nameTooShort: boolean;
      nameTaken: boolean;
    };
    actions: {
      setPermissionSelected: (
        permission: MRole.Permission,
        selected: boolean,
      ) => { permission: MRole.Permission; checked: boolean };
      setName: (name: string) => { name: string };
      setDefault: (isDefault: true | null) => { isDefault: true | null };
      save: true;
    };
  }>
>;

export interface EditRoleDialogProps {
  logicIdentifier: interfaces.ServiceIdentifier<EditRoleLogic>;
  visible: boolean;
  setVisible: (visible: boolean) => void;
  title: string;
  acceptLabel: string;
}

export const EditRoleDialog = ({
  logicIdentifier,
  visible,
  setVisible,
  title,
  acceptLabel,
}: EditRoleDialogProps) => {
  const editRoleLogic = useInjection(logicIdentifier);

  const { saveStatus } = useOptionalValues(editRoleLogic);
  const { save } = useOptionalActions(editRoleLogic);

  const onDialogClose = useCallback(() => {
    setVisible(false);
  }, [setVisible]);

  return (
    <>
      <Dialog
        className={styles.dialog}
        loading={saveStatus == RequestStatus.Running}
        onClose={onDialogClose}
        onAccept={save}
        onReject={onDialogClose}
        acceptLabel={acceptLabel}
        title={title}
        visible={visible}
      >
        <EditRoleDialogBody logicIdentifier={logicIdentifier} />
      </Dialog>
    </>
  );
};

interface EditRoleDialogBodyProps {
  logicIdentifier: interfaces.ServiceIdentifier<EditRoleLogic>;
}

const EditRoleDialogBody = memo(function EditRoleDialogBody({
  logicIdentifier,
}: EditRoleDialogBodyProps) {
  const editRoleLogic = useInjection(logicIdentifier);

  const { setName, setDefault } = useActions(editRoleLogic);
  const { name, isDefault, nameTaken, nameTooShort } = useValues(editRoleLogic);

  const onIsDefaultChange = useCallback(
    ({ checked }: { checked: boolean }) => {
      if (checked) {
        setDefault(true);
      } else {
        setDefault(null);
      }
    },
    [setDefault],
  );

  return (
    <form>
      <TextField
        errorMessage={
          nameTaken
            ? 'role.nameTaken'
            : nameTooShort
            ? 'role.nameTooShort'
            : undefined
        }
        label="role.name"
        value={name}
        onChange={setName}
      />

      <Checkbox
        inputId="default"
        title="role.setDefault"
        className="isDefaultCheckbox"
        checked={isDefault == null ? false : isDefault}
        onChange={onIsDefaultChange}
      />

      <p>
        <Trans>role.permissions</Trans>
      </p>
      <PermissionsList logicIdentifier={logicIdentifier} />
    </form>
  );
});

interface PermissionsListProps {
  logicIdentifier: interfaces.ServiceIdentifier<EditRoleLogic>;
}

const PermissionsList = memo(function PermissionsList({
  logicIdentifier,
}: PermissionsListProps) {
  const editRoleLogic = useInjection(logicIdentifier);
  const roleValidators = useInjection(IRoleValidators.$);

  const { setPermissionSelected } = useActions(editRoleLogic);
  const { selectedPermissions } = useValues(editRoleLogic);

  const onPermissionChange = useCallback(
    ({ value, checked }: { value?: unknown; checked: boolean }) => {
      if (roleValidators.isPermission(value)) {
        setPermissionSelected(value, checked);
      }
    },
    [roleValidators, setPermissionSelected],
  );

  return (
    <div className={styles.permissionsList}>
      {Object.values(MRole.Permission).map((permission) => {
        return (
          <Checkbox
            key={permission}
            inputId={permission}
            className={styles.permissionCheckbox}
            title={`permission.${permission}`}
            value={permission}
            onChange={onPermissionChange}
            checked={selectedPermissions.has(permission)}
          />
        );
      })}
    </div>
  );
});
