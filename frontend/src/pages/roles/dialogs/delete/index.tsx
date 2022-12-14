import { useCallback } from 'react';

import { Dialog } from '@/components/dialog';

import styles from './style.module.scss';

export type DeleteRoleDialogProps = {
  visible: boolean;
  setVisible: (visible: boolean) => void;
};

export const DeleteRoleDialog = ({
  visible,
  setVisible,
}: DeleteRoleDialogProps) => {
  const onDialogClose = useCallback(() => {
    setVisible(false);
  }, [setVisible]);

  return (
    <>
      <Dialog
        onClose={onDialogClose}
        onReject={onDialogClose}
        visible={visible}
      >
        Test
      </Dialog>
    </>
  );
};
