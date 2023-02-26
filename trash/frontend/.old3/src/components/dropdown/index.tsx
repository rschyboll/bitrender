import {
  Dropdown as PrimeDropdown,
  DropdownProps as PrimeDropdownProps,
} from 'primereact/dropdown';
import { memo } from 'react';
import { FiChevronDown } from 'react-icons/fi';

import './style.scss';

export type DropdownProps = PrimeDropdownProps;

export const Dropdown = memo(function Dropdown(props: DropdownProps) {
  return (
    <div className="dropdown">
      <PrimeDropdown className="dropdown-picker" {...props} />
      <FiChevronDown className="dropdown-icon" size={'1.25rem'} />
    </div>
  );
});
