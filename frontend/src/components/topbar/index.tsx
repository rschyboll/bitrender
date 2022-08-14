import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Button } from 'primereact/button';
import { FC } from 'react';

import { Avatar } from '@/components/avatar';
import { Sidebar } from '@/components/sidebar';
import { IAppLogic, IRouteLogic, ISettingsLogic } from '@/logic/interfaces';
import { SidebarType } from '@/types/settings';

import { SidebarDialog } from '../sidebar/dialog';
import './style.scss';

export const Topbar: FC = () => {
  const settingsLogic = useInjection(ISettingsLogic.$);
  const routeLogic = useInjection(IRouteLogic.$);

  const { openUsersPage, openRolesPage } = useActions(routeLogic);

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
          <div className="topbar-content-left">
            <Button onClick={openRolesPage}>Roles</Button>
            <Button onClick={openUsersPage}>Users</Button>
            <Button
              onClick={() => toggleSidebar()}
              className="mobile-sidebar-button"
              icon="ri-menu-line"
            />
          </div>
          <div className="topbar-content-right">
            <div className="topbar-spacer" />
            <Avatar name={'currentUser?.username'} />
            <SidebarDialog active>
              <div />
              <div />
            </SidebarDialog>
          </div>
        </div>
      </div>
    </div>
  );
};
