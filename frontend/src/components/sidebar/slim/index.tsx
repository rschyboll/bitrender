import { useValues } from 'kea';
import { Ripple } from 'primereact/ripple';
import { FC } from 'react';
import { Trans } from 'react-i18next';
import { Link, useLocation } from 'react-router-dom';

import { Logo } from '@/components/logo';
import { settingsLogic } from '@/logic/settings';

import { Group, Item, sidebarModel } from '../model';
import './style.scss';

export const SidebarSlim: FC = () => {
  const location = useLocation();
  const { sidebarType } = useValues(settingsLogic);

  return (
    <div className="sidebar-slim">
      <Logo />
      <ul className="sidebar-container">
        {sidebarModel.map((groupModel) => {
          return <SidebarSlimGroup key={groupModel.title} {...groupModel} />;
        })}
      </ul>
    </div>
  );
};

interface SidebarSlimGroupProps extends Group {}

const SidebarSlimGroup: FC<SidebarSlimGroupProps> = (props) => {
  return (
    <>
      <li className="sidebar-group">
        <div className="sidebar-group-button p-ripple">
          <i className={`sidebar-group-icon pi pi-fw ${props.icon}`} />
          <div className="sidebar-group-title">
            <Trans>{props.title}</Trans>
          </div>
          <Ripple />
        </div>

        <div className="sidebar-group-items"></div>
      </li>
      {props.spacer && <div className="sidebar-spacer" />}
    </>
  );
};

interface SidebarSlimItemProps extends Item {}

const SidebarSlimItem: FC<SidebarSlimItemProps> = (props) => {
  return <Link to={props.path}></Link>;
};
