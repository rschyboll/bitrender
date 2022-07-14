import { memo } from 'react';
import { Trans } from 'react-i18next';

import { Logo } from '@/components/logo';

import { SidebarItem } from '../item';
import { Group, sidebarModel } from '../model';
import './style.scss';

export const SidebarMobile = memo(function SidebarMobile() {
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

type SidebarMobileGroupProps = Group;

const SidebarMobileGroup = memo(function SidebarMobileGroup(
  props: SidebarMobileGroupProps,
) {
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
