import { useInjection } from 'inversify-react';
import { useActions } from 'kea';
import { Ripple } from 'primereact/ripple';
import { memo, useCallback } from 'react';
import { Trans } from 'react-i18next';
import { Link, useLocation } from 'react-router-dom';

import { ISettingsLogic } from '@/logic/interfaces';

import { Item } from '../model';
import './style.scss';

export type SidebarItemProps = Item;

export const SidebarItem = memo(function SidebarItem(props: SidebarItemProps) {
  const settingsLogic = useInjection(ISettingsLogic.$);

  const { toggleSidebar } = useActions(settingsLogic);

  const location = useLocation();

  const onClick = useCallback(() => {
    toggleSidebar(false);
  }, [toggleSidebar]);

  return (
    <Link
      onClick={onClick}
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
