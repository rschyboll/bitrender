import { useActions } from 'kea';
import { Button } from 'primereact/button';
import { FC } from 'react';

import Dependencies from '@/deps';
import { ISettingsLogic } from '@/logic/interfaces';
import { SidebarType } from '@/logic/settings/types';

import { Sidebar } from '../sidebar';
import './style.scss';

export const Topbar: FC = () => {
  const settingsLogic: ISettingsLogic = Dependencies.use('LOGIC', 'SETTINGS');
  const { toggleSidebar } = useActions(settingsLogic);

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
        <div className="topbar-content">
          <Button
            onClick={() => toggleSidebar()}
            className="mobile-sidebar-button"
            icon="ri-menu-line"
          />
        </div>
      </div>
    </div>
  );
};
