import {
  Checkbox as PrimeCheckbox,
  CheckboxProps as PrimeCheckboxProps,
} from 'primereact/checkbox';
import { memo } from 'react';
import { Trans } from 'react-i18next';
import { FiCheck } from 'react-icons/fi';

import styles from './style.module.scss';

export interface CheckboxProps extends Omit<PrimeCheckboxProps, 'className'> {
  classNames?: {
    field?: string;
    checkbox?: string;
    label?: string;
  };
}

export const Checkbox = memo(function Checkbox(props: CheckboxProps) {
  return (
    <div className={`${styles.fieldCheckbox} ${props.classNames?.field || ''}`}>
      <PrimeCheckbox
        className={`${props.classNames?.checkbox || ''}`}
        inputId={props.inputId}
        value={props.value}
        onChange={props.onChange}
        checked={props.checked}
        icon={
          <FiCheck style={{ top: '1px' }} size="18px" className={styles.icon} />
        }
        disabled={props.disabled}
      ></PrimeCheckbox>
      <Label {...props} className={props.classNames?.label} />
    </div>
  );
});

interface LabelProps {
  title?: string;
  inputId?: string;
  className?: string;
}

const Label = memo(function Label(props: LabelProps) {
  return (
    <label
      htmlFor={props.inputId}
      className={`p-checkbox-label ${props.className || ''}`}
    >
      <Trans>{props.title}</Trans>
    </label>
  );
});
