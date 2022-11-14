import { Checkbox as PrimeCheckbox } from 'primereact/checkbox';
import { memo } from 'react';
import { Trans } from 'react-i18next';
import { FiCheck } from 'react-icons/fi';

import './style.scss';

export interface CheckboxProps {
  inputId: string;
  title: string;
  className?: string;
  checked: boolean;
  value?: unknown;
  onChange: (event: { checked: boolean; value?: unknown }) => void;
}

export const Checkbox = memo(function Checkbox(props: CheckboxProps) {
  return (
    <div
      className={`field-checkbox ${
        props.className != null ? props.className : ''
      }`}
    >
      <PrimeCheckbox
        inputId={props.inputId}
        value={props.value}
        onChange={props.onChange}
        checked={props.checked}
        icon={<FiCheck style={{ top: '1px' }} size="18px" className="icon" />}
      ></PrimeCheckbox>
      <label htmlFor={props.inputId} className="p-checkbox-label">
        <Trans>{props.title}</Trans>
      </label>
    </div>
  );
});
