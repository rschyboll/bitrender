import { FC, memo } from 'react';
import { Trans } from 'react-i18next';

import { Logo } from '@/components/logo';

import { SidebarItem } from '../item';
import { Group, sidebarModel } from '../model';
import './style.scss';

export const SidebarMobile: FC = memo(() => {
  return (
    <div className="sidebar-mobile select-none">
      <Logo titleVisible={true} />
      <ul className="sidebar-container">
        {sidebarModel.map((groupModel) => {
          return <SidebarMobileGroup key={groupModel.title} {...groupModel} />;
        })}
      </ul>
    </div>
  );
});

interface SidebarMobileGroupProps extends Group {}

const SidebarMobileGroup: FC<SidebarMobileGroupProps> = memo((props) => {
  return (
    <li className="sidebar-group">
      <span className="sidebar-group-title">
        <Trans>{props.title}</Trans>
      </span>
      <div className="sidebar-group-container">
        {props.items.map((item) => {
          return <SidebarItem key={item.path} {...item} />;
        })}
      </div>
      {props.spacer && <div className="sidebar-spacer" />}
    </li>
  );
});
