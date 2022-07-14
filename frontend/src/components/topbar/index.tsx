import { useActions } from 'kea';
import { Button } from 'primereact/button';
import { FC } from 'react';

import { SidebarType } from '@/logic/core/settings/types';
import { ISettingsLogic } from '@/logic/interfaces';

import { Sidebar } from '../sidebar';
import './style.scss';
import { useInjection } from 'inversify-react';

export const Topbar: FC = () => {
  const settingsLogic = useInjection(ISettingsLogic.$);
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
