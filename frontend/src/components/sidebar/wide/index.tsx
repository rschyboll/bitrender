import { Ripple } from 'primereact/ripple';
import { FC } from 'react';
import { Trans } from 'react-i18next';
import { Link } from 'react-router-dom';

import { Logo } from '@/components/logo';

import { Group, sidebarModel } from '../model';
import './style.scss';

export const SidebarWide: FC = () => {
  return (
    <div className="sidebar-wide select-none">
      <Logo />
      <ul className="sidebar-container">
        {sidebarModel.map((groupModel) => {
          return <SidebarWideGroup {...groupModel} />;
        })}
      </ul>
    </div>
  );
};

interface SidebarWideGroupProps extends Group {}

const SidebarWideGroup: FC<SidebarWideGroupProps> = (props) => {
  return (
    <li className="sidebar-group">
      <div className="sidebar-group-title">
        <Trans>{`nav.${props.title}`}</Trans>
      </div>
      <div className="sidebar-group-container">
        {props.items.map((item) => {
          return <SidebarWideItem {...item} />;
        })}
      </div>
      {props.spacer && <div className="sidebar-spacer" />}
    </li>
  );
};

interface SidebarWideItemProps {
  icon: string;
  title: string;
  path: string;
}

const SidebarWideItem: FC<SidebarWideItemProps> = (props) => {
  return (
    <Link className="sidebar-item p-ripple" to={props.path}>
      <i className={`sidebar-item-icon pi pi-fw ${props.icon}`} />
      <span className="sidebar-item-title">{props.title}</span>
      <Ripple />
    </Link>
  );
};
