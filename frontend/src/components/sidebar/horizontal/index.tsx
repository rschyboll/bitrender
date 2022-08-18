import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Ripple } from 'primereact/ripple';
import { Skeleton } from 'primereact/skeleton';
import { FC, memo, useMemo, useState } from 'react';
import { Trans } from 'react-i18next';
import { RiArrowDownSLine } from 'react-icons/ri';
import { useLocation } from 'react-router-dom';

import { Logo } from '@/components/logo';
import { IAppLogic, ISettingsLogic } from '@/logic/interfaces';

import { SidebarDialog } from '../dialog';
import { SidebarItem } from '../item';
import { Group, Item, filterVisibleItems, sidebarModel } from '../model';
import './style.scss';

export const SidebarHorizontal: FC = memo(function SidebarHorizontal() {
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
    <div className="sidebar-horizontal">
      <Logo />
      <div className="sidebar-horizontal-separator" />
      <ul className="sidebar-container">
        {sidebarModel.map((groupModel) => {
          return (
            <SidebarHorizontalGroup
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

interface SidebarHorizontalGroupProps extends Group {
  groupKey: string;
  onMouseOver: (key: string) => void;
  active: boolean;
  groupItemActive: boolean;
}

const SidebarHorizontalGroup = memo(function SidebarHorizontalGroup(
  props: SidebarHorizontalGroupProps,
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

  if (!appReady || currentUser == null) {
    return <Skeleton className="sidebar-group-loading" />;
  }

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
        <button
          onMouseOver={() => props.onMouseOver(props.groupKey)}
          className="sidebar-group-button p-ripple"
          onClick={() => toggleSidebar()}
        >
          <props.icon className="sidebar-group-icon pi pi-fw" />
          <div className="sidebar-group-title">
            <Trans>{props.title}</Trans>
          </div>
          <RiArrowDownSLine
            className={`sidebar-group-arrow ${
              props.active && sidebarActive && 'sidebar-group-arrow-active'
            } pi pi-fw ri-arrow-down-s-line`}
          />

          <Ripple />
        </button>
        {sidebarActive && (
          <SidebarDialog active={props.active && sidebarActive}>
            {props.items.map((itemModel) => {
              if (visibleItems.includes(itemModel)) {
                return <SidebarItem key={itemModel.path} {...itemModel} />;
              }
              return <div key={itemModel.path} />;
            })}
          </SidebarDialog>
        )}
      </li>
    </>
  );
});
