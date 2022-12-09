import { useInjection } from 'inversify-react';
import { useActions, useMountedLogic, useValues } from 'kea';
import { Outlet } from 'react-router-dom';

import { Sidebar } from '@/components/sidebar';
import { Topbar } from '@/components/topbar';
import { IAppLogic, ISettingsLogic } from '@/logic/interfaces';
import { SidebarType, layoutTypesClasses } from '@/types/settings';

import './style.scss';

const verticalTypes = [SidebarType.Static, SidebarType.Slim];

export const AppPage = () => {
  const settingsLogic = useInjection(ISettingsLogic.$);
  const appLogic = useInjection(IAppLogic.$);

  useMountedLogic(appLogic);

  const { sidebarType, sidebarActive } = useValues(settingsLogic);
  const { toggleSidebar } = useActions(settingsLogic);
  return (
    <div
      className={`layout ${layoutTypesClasses[sidebarType]} ${
        sidebarActive ? 'layout-mobile-active' : ''
      }`}
    >
      <div className="layout-sidebar">
        <Sidebar sidebarKey="sidebar-vertical" types={verticalTypes} />
      </div>
      <div className="layout-topbar">
        <Topbar />
      </div>
      <div onClick={() => toggleSidebar(false)} className="layout-content">
        <div className="layout-page">
          <Outlet />
        </div>
      </div>
      <div
        onClick={() => toggleSidebar(false)}
        className="layout-content-mask"
      />
    </div>
  );
};
