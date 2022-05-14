import { Ripple } from 'primereact/ripple';
import { FC } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';

export interface SidebarItemProps {
  title: string;
  icon: string;
  path: string;
  current: boolean;
}

export const SidebarItem: FC<SidebarItemProps> = (props) => {
  const { t } = useTranslation();

  return (
    <Link
      to={props.path}
      className={`sidebar-item p-ripple ${
        props.current ? 'sidebar-item-current' : ''
      }`}
    >
      <i className={`pi ${props.icon}`} />
      <span>{t(props.title)}</span>
      <Ripple />
    </Link>
  );
};
