import { Ripple } from 'primereact/ripple';
import { FC } from 'react';
import { Trans } from 'react-i18next';
import { Link, useLocation } from 'react-router-dom';

import { Logo } from '@/components/logo';

import { Group, Item, sidebarModel } from '../model';
import './style.scss';

export const SidebarWide: FC = () => {
  return (
    <div className="sidebar-wide select-none">
      <Logo titleVisible={true} />
      <ul className="sidebar-container">
        {sidebarModel.map((groupModel) => {
          return <SidebarWideGroup key={groupModel.title} {...groupModel} />;
        })}
      </ul>
    </div>
  );
};

interface SidebarWideGroupProps extends Group {}

const SidebarWideGroup: FC<SidebarWideGroupProps> = (props) => {
  return (
    <li className="sidebar-group">
      <span className="sidebar-group-title">
        <Trans>{props.title}</Trans>
      </span>
      <div className="sidebar-group-container">
        {props.items.map((item) => {
          return <SidebarWideItem key={item.path} {...item} />;
        })}
      </div>
      {props.spacer && <div className="sidebar-spacer" />}
    </li>
  );
};

interface SidebarWideItemProps extends Item {}

const SidebarWideItem: FC<SidebarWideItemProps> = (props) => {
  const location = useLocation();

  return (
    <Link
      draggable={false}
      className={`sidebar-item p-ripple ${
        location.pathname == props.path && 'sidebar-item-active'
      }`}
      to={props.path}
    >
      <i className={`sidebar-item-icon pi pi-fw ${props.icon}`} />
      <span className="sidebar-item-title">{props.title}</span>
      <Ripple />
    </Link>
  );
};
