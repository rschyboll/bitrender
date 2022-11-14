import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Button } from 'primereact/button';
import { memo, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { RiCloseFill } from 'react-icons/ri';

import { Checkbox } from '@/components/checkbox';
import { TextField } from '@/components/textField';
import { ICreateRoleLogic } from '@/logic/interfaces';
import { RequestStatus } from '@/services';
import { MRole } from '@/types/models';
import { IRoleValidators } from '@/validators/interfaces';

import './style.scss';

export const CreateRoleDialog = memo(function ModifyColumn() {
  const createRoleLogic = useInjection(ICreateRoleLogic.$);
  const roleValidators = useInjection(IRoleValidators.$);

  const { setName, setPermissionSelected, setDefault } =
    useActions(createRoleLogic);
  const { name, selectedPermissions, isDefault } = useValues(createRoleLogic);

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

  const onPermissionChange = useCallback(
    ({ value, checked }: { value?: unknown; checked: boolean }) => {
      console.log(value);
      if (roleValidators.isPermission(value)) {
        console.log(value);
        setPermissionSelected(value, checked);
      }
    },
    [roleValidators, setPermissionSelected],
  );

  return (
    <form className="create-role-dialog">
      <TextField label="Nazwa" value={name} onChange={setName} />

      <Checkbox
        inputId="default"
        title="role.setDefault"
        checked={isDefault == null ? false : isDefault}
        onChange={onIsDefaultChange}
      />

      <p className="role-permissions-title">Uprawnienia:</p>
      <div className="permissions-list">
        {Object.values(MRole.Permission).map((permission) => {
          return (
            <Checkbox
              key={permission}
              inputId={permission}
              title={`permission.${permission}`}
              value={permission}
              onChange={onPermissionChange}
              checked={selectedPermissions.has(permission)}
            />
          );
        })}
      </div>

      <div className="footer-buttons"></div>
    </form>
  );
});

export interface CreateDialogFooterProps {
  closeDialog: () => void;
}

export const CreateDialogFooter = memo(function CreateDialogFooter(
  props: CreateDialogFooterProps,
) {
  const { t } = useTranslation();

  const createRoleLogic = useInjection(ICreateRoleLogic.$);

  const { save } = useActions(createRoleLogic);
  const { saveStatus } = useValues(createRoleLogic);

  console.log(saveStatus);

  return (
    <>
      <Button
        className="p-button-text"
        label={t('cancel')}
        onClick={props.closeDialog}
        disabled={saveStatus == RequestStatus.Running}
      />
      <Button
        className="p-button-text"
        label={t('create')}
        onClick={save}
        disabled={saveStatus == RequestStatus.Running}
      />
    </>
  );
});

export interface CreateDialogIconsProps {
  closeDialog: () => void;
}

export const CreateDialogIcons = memo(function CreateDialogIcons(
  props: CreateDialogIconsProps,
) {
  const addRoleLogic = useInjection(ICreateRoleLogic.$);

  const { saveStatus } = useValues(addRoleLogic);

  const onClick = useCallback(() => {
    if (saveStatus == RequestStatus.Running) {
      return;
    }
    props.closeDialog();
  }, [props, saveStatus]);

  return (
    <Button
      className="p-button-text p-button-rounded p-button-plain"
      icon={<RiCloseFill />}
      onClick={onClick}
      disabled={saveStatus == RequestStatus.Running}
    />
  );
});
