import { useInjection } from 'inversify-react';
import { BuiltLogic, LogicWrapper, useActions, useValues } from 'kea';
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

type EditRoleLogic = MakeOwnLogicType<{
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  props: any;
  values: {
    name: string;
    selectedPermissions: Set<MRole.Permission>;
    isDefault: boolean | null;
    saveStatus: RequestStatus;
    nameTooShort: boolean;
    nameTaken: boolean;
    isDefaultLocked?: boolean;
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
}>;

export type EditRoleDialogProps = {
  logic: LogicWrapper<EditRoleLogic> | BuiltLogic<EditRoleLogic>;
  visible: boolean;
  setVisible: (visible: boolean) => void;
  title: string;
  acceptLabel: string;
};

export const EditRoleDialog = ({
  logic,
  visible,
  setVisible,
  title,
  acceptLabel,
}: EditRoleDialogProps) => {
  const editRoleLogic = logic;

  const { saveStatus } = useOptionalValues(editRoleLogic);
  const { save } = useOptionalActions(editRoleLogic);

  const onDialogClose = useCallback(() => {
    setVisible(false);
  }, [setVisible]);

  return (
    <>
      <Dialog
        className={styles.dialog}
        closeDisabled={saveStatus == RequestStatus.Running}
        acceptDisabled={saveStatus == RequestStatus.Running}
        onHide={onDialogClose}
        onAccept={save}
        acceptLabel={acceptLabel}
        title={title}
        visible={visible}
      >
        <EditRoleDialogBody logic={logic} />
      </Dialog>
    </>
  );
};

interface EditRoleDialogBodyProps {
  logic: LogicWrapper<EditRoleLogic> | BuiltLogic<EditRoleLogic>;
}

const EditRoleDialogBody = memo(function EditRoleDialogBody({
  logic,
}: EditRoleDialogBodyProps) {
  const editRoleLogic = logic;

  const { setName, setDefault } = useActions(editRoleLogic);
  const { name, isDefault, nameTaken, nameTooShort, isDefaultLocked } =
    useValues(editRoleLogic);

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
        classNames={{ field: 'isDefaultCheckbox' }}
        checked={isDefault == null ? false : isDefault}
        onChange={onIsDefaultChange}
        disabled={isDefaultLocked}
      />

      <p>
        <Trans>role.permissions</Trans>
      </p>
      <PermissionsList logic={logic} />
    </form>
  );
});

interface PermissionsListProps {
  logic: LogicWrapper<EditRoleLogic> | BuiltLogic<EditRoleLogic>;
}

const PermissionsList = memo(function PermissionsList({
  logic,
}: PermissionsListProps) {
  const editRoleLogic = logic;
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
            classNames={{ field: styles.permissionCheckbox }}
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
