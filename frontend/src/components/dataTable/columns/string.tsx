import { Column as PrimeColumn } from 'primereact/column';
import { useTranslation } from 'react-i18next';

import { ColumnProps } from '.';

export const StringColumn = (props: ColumnProps) => {
  const { t } = useTranslation();

  return <PrimeColumn key={props.key} header={t(props.title)} />;
};
