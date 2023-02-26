import { RiCheckboxCircleFill, RiCloseCircleFill } from 'react-icons/ri';

export interface BooleanColumnProps {
  value: boolean;
}

export const BooleanColumn = (props: BooleanColumnProps) => {
  if (props.value != null) {
    return <RiCheckboxCircleFill size="1.5rem" color="var(--success-color)" />;
  } else {
    return <RiCloseCircleFill size="1.5rem" color="var(--danger-color)" />;
  }
};
