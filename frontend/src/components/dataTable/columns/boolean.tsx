import { RiCheckboxCircleFill, RiCloseCircleFill } from 'react-icons/ri';

import styles from './style.module.scss';

export interface BooleanColumnProps {
  value: boolean;
}

export const BooleanColumn = (props: BooleanColumnProps) => {
  if (props.value) {
    return (
      <div className={styles.iconColumn}>
        <RiCheckboxCircleFill
          className={`${styles.iconSize} ${styles.colorSuccess}`}
        />
      </div>
    );
  } else {
    return (
      <div className={styles.iconColumn}>
        <RiCloseCircleFill
          className={`${styles.iconSize} ${styles.colorDanger}`}
        />
      </div>
    );
  }
};
