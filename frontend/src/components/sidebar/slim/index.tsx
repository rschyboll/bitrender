import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Ripple } from 'primereact/ripple';
import { memo, useMemo, useState } from 'react';
import { Trans } from 'react-i18next';
import { useLocation } from 'react-router-dom';

import { Logo } from '@/components/logo';
import { ISettingsLogic } from '@/logic/interfaces';

import { SidebarDialog } from '../dialog';
import { SidebarItem } from '../item';
import { Group, sidebarModel } from '../model';
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

  const { toggleSidebar } = useActions(settingsLogic);
  const { sidebarActive } = useValues(settingsLogic);

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
          <i className={`sidebar-group-icon pi pi-fw ${props.icon}`} />
          <div className="sidebar-group-title">
            <Trans>{props.title}</Trans>
          </div>
          <Ripple />
        </button>
        <SidebarDialog active={props.active && sidebarActive}>
          {props.items.map((itemModel) => {
            return <SidebarItem key={itemModel.path} {...itemModel} />;
          })}
        </SidebarDialog>
      </li>
      {props.spacer && <div className="sidebar-spacer" />}
    </>
  );
});
