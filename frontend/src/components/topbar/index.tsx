import { FC } from 'react';

import { SidebarType } from '@/logic/settings/types';

import { Sidebar } from '../sidebar';
import './style.scss';

export const Topbar: FC = () => {
  return (
    <div className="topbar">
      <div className="topbar-sidebar-background" />
      <div className="topbar-container">
        <div className="topbar-sidebar">
          <Sidebar
            sidebarKey="sidebar-horizontal"
            types={[SidebarType.Horizontal]}
          />
        </div>
        <div className="topbar-content"></div>
      </div>
    </div>
  );
};
