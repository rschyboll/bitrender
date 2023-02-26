import { Password } from 'primereact/password';
import {
  ChangeEvent,
  ReactNode,
  memo,
  useCallback,
  useEffect,
  useState,
} from 'react';
import { Trans } from 'react-i18next';
import { RiEyeFill, RiEyeOffFill, RiLockFill } from 'react-icons/ri';

import './style.scss';

export interface PasswordFieldProps {
  id?: string;
  className?: string;
  inputId: string;
  inputClassName?: string;
  value: string;
  onChange: (value: string) => void;
  label?: string;
  errorMessage?: string;
  floorLeftContent?: ReactNode;
  floorRightContent?: ReactNode;
  mediumRegex?: string;
  strongRegex?: string;
}

export const PasswordField = memo(function PasswordField(
  props: PasswordFieldProps,
) {
  const {
    id,
    className,
    inputId,
    inputClassName,
    value,
    onChange,
    label,
    errorMessage,
    mediumRegex,
    strongRegex,
  } = props;

  const [passwordVisible, setPasswordVisible] = useState(false);

  const onInputChange = useCallback(
    (e: ChangeEvent<HTMLInputElement>) => onChange(e.target.value),
    [onChange],
  );

  const togglePasswordVisibility = useCallback(() => {
    setPasswordVisible(!passwordVisible);
  }, [setPasswordVisible, passwordVisible]);

  useEffect(() => {
    const passwordInput = document.getElementById(inputId)?.firstChild;
    if (passwordInput instanceof HTMLInputElement) {
      if (passwordVisible) {
        passwordInput.type = 'text';
      } else {
        passwordInput.type = 'password';
      }
    }
  }, [inputId, passwordVisible]);

  return (
    <div id={id} className={`field password-field ${className}`}>
      {/*   PasswordField label   */}
      {label != null ? (
        <label htmlFor={inputId != null ? inputId : undefined}>
          <Trans>{label}</Trans>
        </label>
      ) : null}

      {/*   PasswordField body   */}
      <span className="password-field-body p-input-icon-left p-input-icon-right">
        {/*   PasswordField left icon   */}
        <RiLockFill className="password-field-icon password-field-left-icon" />

        {/*   PasswordField input   */}
        <Password
          id={inputId}
          className={`password-field-input ${inputClassName} ${
            errorMessage != null ? 'p-invalid' : ''
          }`}
          value={value}
          onChange={onInputChange}
          mediumRegex={mediumRegex}
          strongRegex={strongRegex}
        />
        {/*   PasswordField right icon   */}
        {passwordVisible ? (
          <RiEyeFill
            onClick={togglePasswordVisibility}
            className="password-field-icon password-field-right-icon"
          />
        ) : (
          <RiEyeOffFill
            onClick={togglePasswordVisibility}
            className="password-field-icon password-field-right-icon"
          />
        )}
      </span>

      {/*   PasswordField errorMessage   */}
      <div className="password-field-floor">
        {props.errorMessage != null ? (
          <span className="p-error password-field-error-message">
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
