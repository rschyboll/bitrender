import { RiCheckboxCircleFill, RiCloseCircleFill } from 'react-icons/ri';

import styles from './style.module.scss';

export interface TrueOrNullColumnProps {
  value: true | null;
}

export const TrueOrNullColumn = (props: TrueOrNullColumnProps) => {
  if (props.value != null) {
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
