import { Button } from 'primereact/button';
import { Dialog as PrimeDialog } from 'primereact/dialog';
import { ReactNode, memo, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { RiCloseFill, RiLoader4Fill } from 'react-icons/ri';

import style from './style.module.scss';

export interface DialogProps {
  visible: boolean;
  loading?: boolean;
  onAccept?: () => void;
  onReject?: () => void;
  acceptLabel?: string;
  rejectLabel?: string;
  onClose?: () => void;
  title?: string;
  className?: string;
  children: ReactNode;
}

export const Dialog = memo(function Dialog({
  visible,
  loading,
  onAccept,
  onReject,
  acceptLabel,
  rejectLabel,
  onClose,
  title,
  children,
  className,
}: DialogProps) {
  const { t } = useTranslation();

  const onHideCallback = useCallback(() => {
    if (onClose != null) {
      onClose();
    }
  }, [onClose]);

  return (
    <PrimeDialog
      className={`${style.dialog} ${className}`}
      onHide={onHideCallback}
      visible={visible}
      closable={false}
      dismissableMask={!loading}
      icons={
        onClose != null ? (
          <DialogCloseIcon onClose={onClose} loading={loading} />
        ) : null
      }
      header={title != null ? t(title) : undefined}
      footer={
        <DialogFooterButtons
          onAccept={onAccept}
          onReject={onReject}
          acceptLabel={acceptLabel}
          rejectLabel={rejectLabel}
          loading={loading}
        />
      }
    >
      <div className={loading == true ? style.loading : undefined}>
        {children}
      </div>
      <div
        className={`${style.loadingOverlay} ${
          loading == true ? style.visible : undefined
        }`}
      >
        <RiLoader4Fill className={style.loadingIcon} />
      </div>
    </PrimeDialog>
  );
});

interface DialogFooterButtonsProps {
  onAccept?: () => void;
  onReject?: () => void;
  acceptLabel?: string;
  rejectLabel?: string;
  loading?: boolean;
}

const DialogFooterButtons = memo(function DialogFooterButtons({
  onAccept,
  onReject,
  acceptLabel,
  rejectLabel,
  loading,
}: DialogFooterButtonsProps) {
  const { t } = useTranslation();

  return (
    <div className={style.footerButtonsContainer}>
      {onReject != null ? (
        <Button
          className="p-button-text"
          label={t(rejectLabel != null ? rejectLabel : 'cancel')}
          onClick={onReject}
          disabled={loading == true}
        />
      ) : null}
      {onAccept != null ? (
        <Button
          className="p-button-text"
          label={t(acceptLabel != null ? acceptLabel : 'accept')}
          onClick={onAccept}
          disabled={loading == true}
        />
      ) : null}
    </div>
  );
});

interface DialogCloseIconProps {
  onClose: () => void;
  loading?: boolean;
}

const DialogCloseIcon = memo(function DialogCloseIcon({
  onClose,
  loading,
}: DialogCloseIconProps) {
  return (
    <Button
      className="p-button-text p-button-rounded p-button-plain"
      icon={<RiCloseFill />}
      onClick={onClose}
      disabled={loading == true}
    />
  );
});
