import { useInjection } from 'inversify-react';
import { useActions, useMountedLogic, useValues } from 'kea';
import { memo } from 'react';
import { Outlet } from 'react-router-dom';

import { Sidebar } from '@/components/sidebar';
import { Topbar } from '@/components/topbar';
import { testLogic } from '@/logic/core/test';
import { ISettingsLogic } from '@/logic/interfaces';
import { SidebarType, layoutTypesClasses } from '@/types/settings';

import './style.scss';

const verticalTypes = [SidebarType.Static, SidebarType.Slim];

export const AppPage = memo(function AppPage() {
  const settingsLogic = useInjection(ISettingsLogic.$);

  const { sidebarType, sidebarActive } = useValues(settingsLogic);
  const { toggleSidebar } = useActions(settingsLogic);

  useMountedLogic(testLogic);

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
});
