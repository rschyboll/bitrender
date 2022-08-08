import { memo } from 'react';
import { Trans } from 'react-i18next';
import { IconType } from 'react-icons';

export interface TextFieldProps {
  id?: string;
  className?: string;
  value: string;
  onChange: (value: string) => void;
  label?: string;
  errorMessage?: string;
  leftIcon?: IconType;
  rightIcon?: IconType;
  onLeftIconClick?: () => void;
  onRightIconClick?: () => void;
}

export const TextField = memo(function TextField(props: TextFieldProps) {
  return (
    <div id={props.id} className={`field text-field ${props.className}`}>
      {props.label != null ? (
        <label htmlFor={props.id != null ? props.id : undefined}>
          <Trans>{props.label}</Trans>
        </label>
      ) : null}
      <span className="p-input-icon-left p-input-icon-right"></span>
    </div>
  );
});
