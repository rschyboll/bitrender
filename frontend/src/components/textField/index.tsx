import { InputText } from 'primereact/inputtext';
import {
  ChangeEvent,
  HTMLInputTypeAttribute,
  ReactNode,
  memo,
  useCallback,
} from 'react';
import { Trans } from 'react-i18next';
import { IconType } from 'react-icons';

import './style.scss';

export interface TextFieldProps {
  id?: string;
  className?: string;
  inputId?: string;
  inputClassName?: string;
  value: string;
  onChange: (value: string) => void;
  label?: string;
  type?: HTMLInputTypeAttribute;
  errorMessage?: string;
  floorLeftContent?: ReactNode;
  floorRightContent?: ReactNode;
  leftIcon?: IconType;
  rightIcon?: IconType;
  onLeftIconClick?: () => void;
  onRightIconClick?: () => void;
}

export const TextField = memo(function TextField(props: TextFieldProps) {
  const {
    id,
    className,
    inputId,
    inputClassName,
    value,
    onChange,
    label,
    type,
    errorMessage,
    onLeftIconClick,
    onRightIconClick,
  } = props;

  const onInputChange = useCallback(
    (e: ChangeEvent<HTMLInputElement>) => onChange(e.target.value),
    [onChange],
  );

  return (
    <div id={id} className={`field text-field ${className}`}>
      {/*   TextField label   */}
      {label != null ? (
        <label htmlFor={inputId != null ? inputId : undefined}>
          <Trans>{label}</Trans>
        </label>
      ) : null}

      {/*   TextField body   */}
      <span className="text-field-body p-input-icon-left p-input-icon-right">
        {/*   TextField left icon   */}
        {props.leftIcon != null ? (
          <props.leftIcon
            className={`text-field-icon text-field-left-icon ${
              onLeftIconClick != null ? 'clickable' : ''
            }`}
            onClick={onLeftIconClick}
          />
        ) : null}

        {/*   TextField input   */}
        <InputText
          id={inputId}
          className={`text-field-input ${inputClassName} ${
            errorMessage != null ? 'p-invalid' : ''
          }`}
          value={value}
          onChange={onInputChange}
          type={type}
        />

        {/*   TextField right icon   */}
        {props.rightIcon != null ? (
          <props.rightIcon
            className={`text-field-icon text-field-right-icon ${
              onRightIconClick != null ? 'clickable' : ''
            }`}
            onClick={onRightIconClick}
          />
        ) : null}
      </span>

      {/*   TextField errorMessage   */}

      <div className="text-field-floor">
        {props.errorMessage != null ? (
          <span className="p-error text-field-error-message">
            <Trans>{props.errorMessage}</Trans>
          </span>
        ) : props.floorLeftContent != null ? (
          props.floorLeftContent
        ) : (
          <div />
        )}
        {props.floorRightContent}
      </div>
    </div>
  );
});
