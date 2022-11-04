import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Ripple } from 'primereact/ripple';
import { Skeleton } from 'primereact/skeleton';
import { memo, useMemo, useState } from 'react';
import { Trans } from 'react-i18next';
import { useLocation } from 'react-router-dom';

import { Logo } from '@/components/logo';
import { IAppLogic, ISettingsLogic } from '@/logic/interfaces';

import { SidebarDialog } from '../dialog';
import { SidebarItem } from '../item';
import { Group, filterVisibleItems, sidebarModel } from '../model';
import './style.scss';

export const SidebarSlim = memo(function SidebarSlim() {
  const [activeGroup, setActiveGroup] = useState<string | null>(null);

  const location = useLocation();

  const currentGroup = useMemo(() => {
    return Object.values(sidebarModel).find((group) => {
      return (
        group.items.find((item) => item.path == location.pathname) != undefined
      );
    });
  }, [location]);

  return (
    <div className="sidebar-slim">
      <Logo />
      <ul className="sidebar-container">
        {sidebarModel.map((groupModel) => {
          return (
            <SidebarSlimGroup
              key={groupModel.title}
              groupKey={groupModel.title}
              onMouseOver={setActiveGroup}
              active={activeGroup == groupModel.title}
              groupItemActive={currentGroup == groupModel}
              {...groupModel}
            />
          );
        })}
      </ul>
    </div>
  );
});

interface SidebarSlimGroupProps extends Group {
  groupKey: string;
  onMouseOver: (key: string) => void;
  active: boolean;
  groupItemActive: boolean;
}

const SidebarSlimGroup = memo(function SidebarSlimGroup(
  props: SidebarSlimGroupProps,
) {
  const settingsLogic = useInjection(ISettingsLogic.$);
  const appLogic = useInjection(IAppLogic.$);

  const { toggleSidebar } = useActions(settingsLogic);
  const { sidebarActive } = useValues(settingsLogic);

  const { appReady, currentUser } = useValues(appLogic);

  const visibleItems = useMemo(
    () => filterVisibleItems(props.items, currentUser?.permissions),
    [currentUser, props.items],
  );

  if (visibleItems.length == 0) {
    return null;
  }

  return (
    <>
      <li
        className={`sidebar-group ${
          props.groupItemActive && 'sidebar-group-active'
        }`}
      >
        {!(!appReady || currentUser == null) ? (
          <>
            <button
              onMouseOver={() => props.onMouseOver(props.groupKey)}
              className="sidebar-group-button p-ripple"
              onClick={() => toggleSidebar()}
            >
              <props.icon className="sidebar-group-icon pi pi-fw" />
              <div className="sidebar-group-title">
                <Trans>{props.title}</Trans>
              </div>
              <Ripple />
            </button>
            {sidebarActive && (
              <SidebarDialog active={props.active}>
                {props.items.map((itemModel) => {
                  if (visibleItems.includes(itemModel)) {
                    return <SidebarItem key={itemModel.path} {...itemModel} />;
                  }
                  return <div key={itemModel.path} />;
                })}
              </SidebarDialog>
            )}
          </>
        ) : (
          <Skeleton className="sidebar-group-loading" />
        )}
      </li>
      {props.spacer && <div className="sidebar-spacer" />}
    </>
  );
});
