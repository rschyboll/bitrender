import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Ripple } from 'primereact/ripple';
import { Skeleton } from 'primereact/skeleton';
import { memo, useCallback } from 'react';
import { Trans } from 'react-i18next';
import { Link, useLocation } from 'react-router-dom';

import { IAppLogic, ISettingsLogic } from '@/logic/interfaces';

import { Item } from '../model';
import './style.scss';

export type SidebarItemProps = Item;

export const SidebarItem = memo(function SidebarItem(props: SidebarItemProps) {
  const settingsLogic = useInjection(ISettingsLogic.$);
  const appLogic = useInjection(IAppLogic.$);

  const { toggleSidebar } = useActions(settingsLogic);
  const { appReady } = useValues(appLogic);

  const onClick = useCallback(() => {
    toggleSidebar(false);
  }, [toggleSidebar]);

  if (!appReady) {
    return <Skeleton className="sidebar-item-loading" />;
  }
  
  const location = useLocation();

  return (
    <Link
      onClick={onClick}
      draggable={false}
      className={`sidebar-item p-ripple ${
        location.pathname == props.path && 'sidebar-item-active'
      }`}
      to={props.path}
    >
      <div className="sidebar-item-icon-container">
        <props.icon
          style={{
            top:
              props.iconSize != null
                ? `calc((1.2rem - ${props.iconSize})/2)`
                : undefined,
            left:
              props.iconSize != null
                ? `calc((1.2rem - ${props.iconSize})/2)`
                : undefined,
          }}
          size={props.iconSize != null ? props.iconSize : '1.2rem'}
          className="sidebar-item-icon"
        />
      </div>

      <span className="sidebar-item-title">
        <Trans>{props.title}</Trans>
      </span>
      <Ripple />
    </Link>
  );
});
