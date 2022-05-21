import { useActions } from 'kea';
import { Ripple } from 'primereact/ripple';
import { FC, memo } from 'react';
import { Trans } from 'react-i18next';
import { Link, useLocation } from 'react-router-dom';

import { settingsLogic } from '@/logic/settings';

import { Item } from '../model';
import './style.scss';

export interface SidebarItemProps extends Item {}

export const SidebarItem: FC<SidebarItemProps> = memo((props) => {
  const location = useLocation();
  const { setSlimSidebarState } = useActions(settingsLogic);

  return (
    <Link
      onClick={() => setSlimSidebarState(false)}
      draggable={false}
      className={`sidebar-item p-ripple ${
        location.pathname == props.path && 'sidebar-item-active'
      }`}
      to={props.path}
    >
      <i className={`sidebar-item-icon pi pi-fw ${props.icon}`} />
      <span className="sidebar-item-title">
        <Trans>{props.title}</Trans>
      </span>
      <Ripple />
    </Link>
  );
});
