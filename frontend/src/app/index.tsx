import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Button } from 'primereact/button';
import { FC, useEffect } from 'react';
import { Outlet, Route, Routes } from 'react-router-dom';

import { Sidebar } from '@/components/sidebar';
import { Topbar } from '@/components/topbar';
import { SERVICE } from '@/deps';
import { SettingsLogic } from '@/logic/interfaces/settings';
import { SidebarType, Theme } from '@/logic/settings/types';
import { RolesPage } from '@/pages/roles';
import { UsersPage } from '@/pages/users';

import './style.scss';

const layoutTypesClasses = {
  [SidebarType.Horizontal]: 'layout-horizontal',
  [SidebarType.Slim]: 'layout-slim',
  [SidebarType.Static]: 'layout-static',
};

const themeClasses = {
  [Theme.Dark]: 'dark',
  [Theme.Dim]: 'dim',
  [Theme.Light]: 'light',
};

const verticalTypes = [SidebarType.Static, SidebarType.Slim];

export const App: FC = () => {
  const settingsLogic: SettingsLogic = useInjection(SERVICE.SETTINGS_LOGIC);
  const { theme } = useValues(settingsLogic);

  useEffect(() => {
    const themeLink = document.getElementById('theme-link');
    if (themeLink instanceof HTMLLinkElement) {
      themeLink.href = `themes/${themeClasses[theme]}.css`;
    }
  }, [theme]);

  return (
    <Routes>
      <Route path="/" element={<AppBody />}>
        <Route path="users" element={<UsersPage />} />
        <Route path="roles" element={<RolesPage />} />
      </Route>
    </Routes>
  );
};

export const AppBody: FC = () => {
  const settingsLogic: SettingsLogic = useInjection(SERVICE.SETTINGS_LOGIC);

  const { sidebarType, theme, sidebarActive } = useValues(settingsLogic);
  const { setSidebarType, setTheme, toggleSidebar } = useActions(settingsLogic);

  return (
    <div
      className={`layout ${layoutTypesClasses[sidebarType]} theme-${
        themeClasses[theme]
      } ${sidebarActive ? 'layout-mobile-active' : ''}`}
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
        <Button label="Slim" onClick={() => setSidebarType(SidebarType.Slim)} />
        <Button
          label="Static"
          onClick={() => setSidebarType(SidebarType.Static)}
        />
        <Button
          label="Horizontal"
          onClick={() => setSidebarType(SidebarType.Horizontal)}
        />
        <Button label="Dark" onClick={() => setTheme(Theme.Dark)} />
        <Button label="Dim" onClick={() => setTheme(Theme.Dim)} />
        <Button label="Light" onClick={() => setTheme(Theme.Light)} />{' '}
      </div>
      <div className="layout-content-mask" />
    </div>
  );
};
