import { Button } from 'primereact/button';
import {
  Dialog as PrimeDialog,
  DialogProps as PrimeDialogProps,
} from 'primereact/dialog';
import { memo } from 'react';
import { RiCloseFill } from 'react-icons/ri';

import style from './style.module.scss';

export interface DialogProps extends PrimeDialogProps {
  acceptDisabled?: boolean;
  closeDisabled?: boolean;
  hideHeader?: boolean;
  hideFooter?: boolean;
  onAccept?: () => void;
  onReject?: () => void;
  acceptLabel?: string;
  rejectLabel?: string;
  title?: string;
  closeIconClassName?: string;
}

export const Dialog = memo(function Dialog(props: DialogProps) {
  const {
    acceptDisabled,
    closeDisabled,
    hideHeader,
    hideFooter,
    onAccept,
    onReject,
    acceptLabel,
    rejectLabel,
    title,
    closeIconClassName,
    ...primeProps
  } = props;

  return (
    <PrimeDialog
      {...primeProps}
      closable={false}
      dismissableMask={!closeDisabled}
      icons={
        !hideHeader ? (
          <DialogCloseIcon
            className={closeIconClassName}
            onClose={props.onHide}
          />
        ) : undefined
      }
      header={!hideHeader ? title : undefined}
      footer={
        !hideFooter ? (
          <DialogFooterButtons
            onAccept={onAccept}
            onReject={onReject}
            acceptLabel={acceptLabel}
            rejectLabel={rejectLabel}
            acceptDisabled={acceptDisabled}
            rejectDisabled={closeDisabled}
          />
        ) : undefined
      }
    >
      {props.children}
    </PrimeDialog>
  );
});

interface DialogFooterButtonsProps {
  onAccept?: () => void;
  onReject?: () => void;
  acceptLabel?: string;
  rejectLabel?: string;
  acceptDisabled?: boolean;
  rejectDisabled?: boolean;
}

const DialogFooterButtons = memo(function DialogFooterButtons(
  props: DialogFooterButtonsProps,
) {
  return (
    <div className={style.footerButtonsContainer}>
      {props.onReject != null ? (
        <Button
          className="p-button-text"
          label={props.rejectLabel}
          onClick={props.onReject}
          disabled={props.rejectDisabled}
        />
      ) : null}
      {props.onAccept != null ? (
        <Button
          className="p-button-text"
          label={props.acceptLabel}
          onClick={props.onAccept}
          disabled={props.acceptDisabled}
        />
      ) : null}
    </div>
  );
});

interface DialogCloseIconProps {
  onClose: () => void;
  disabled?: boolean;
  className?: string;
}

const DialogCloseIcon = memo(function DialogCloseIcon(
  props: DialogCloseIconProps,
) {
  return (
    <Button
      className={`${
        props.className || ''
      } p-button-text p-button-rounded p-button-plain`}
      icon={<RiCloseFill />}
      onClick={props.onClose}
      disabled={props.disabled}
    />
  );
});
