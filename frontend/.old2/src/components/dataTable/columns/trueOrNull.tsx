import { RiCheckboxCircleFill, RiCloseCircleFill } from 'react-icons/ri';

export interface TrueOrNullColumnProps {
  value: true | null;
}

export const TrueOrNullColumn = (props: TrueOrNullColumnProps) => {
  if (props.value != null) {
    return <RiCheckboxCircleFill size="1.5rem" color="var(--success-color)" />;
  } else {
    return <RiCloseCircleFill size="1.5rem" color="var(--danger-color)" />;
  }
};
