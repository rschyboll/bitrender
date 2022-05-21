import { useActions, useValues } from 'kea';
import { Ripple } from 'primereact/ripple';
import { FC, memo, useMemo, useState } from 'react';
import { Trans } from 'react-i18next';
import { useLocation } from 'react-router-dom';
import { CSSTransition, SwitchTransition } from 'react-transition-group';

import { Logo } from '@/components/logo';
import { settingsLogic } from '@/logic/settings';

import { SidebarItem } from '../item';
import { Group, sidebarModel } from '../model';
import './style.scss';

export const SidebarSlim: FC = memo(() => {
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

const SidebarSlimGroup: FC<SidebarSlimGroupProps> = memo((props) => {
  const { setSlimSidebarState } = useActions(settingsLogic);
  const { sidebarSlimActive } = useValues(settingsLogic);

  return (
    <>
      <li
        className={`sidebar-group ${
          props.groupItemActive && 'sidebar-group-active'
        }`}
      >
        <div
          onMouseOver={() => props.onMouseOver(props.groupKey)}
          className="sidebar-group-button p-ripple"
          onClick={() => setSlimSidebarState(!sidebarSlimActive)}
        >
          <i className={`sidebar-group-icon pi pi-fw ${props.icon}`} />
          <div className="sidebar-group-title">
            <Trans>{props.title}</Trans>
          </div>
          <Ripple />
        </div>
        <SwitchTransition>
          <CSSTransition
            addEndListener={() => {}}
            classNames="sidebar-items-fade"
            key={
              props.active && sidebarSlimActive
                ? props.groupKey
                : `${props.groupKey}-hidden`
            }
            timeout={75}
            unmountOnExit
            mountOnEnter
          >
            {props.active && sidebarSlimActive ? (
              <div className="sidebar-group-items">
                {props.items.map((itemModel) => {
                  return <SidebarItem key={itemModel.path} {...itemModel} />;
                })}
              </div>
            ) : (
              <div />
            )}
          </CSSTransition>
        </SwitchTransition>
      </li>
      {props.spacer && <div className="sidebar-spacer" />}
    </>
  );
});
