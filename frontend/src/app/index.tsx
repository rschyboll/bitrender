import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Button } from 'primereact/button';
import { Slider } from 'primereact/slider';
import { FC } from 'react';
import { Outlet, Route, Routes } from 'react-router-dom';

import { Sidebar } from '@/components/sidebar';
import { Topbar } from '@/components/topbar';
import { ISettingsLogic } from '@/logic/interfaces';
import { LoginPage, RolesPage, UsersPage } from '@/pages';
import {
  SidebarType,
  Theme,
  layoutTypesClasses,
  themeClasses,
} from '@/types/settings';

import './style.scss';

const verticalTypes = [SidebarType.Static, SidebarType.Slim];

export const App: FC = () => {
  return (
    <Routes>
      <Route path="/" element={<AppContainer />}>
        <Route path="app" element={<AppLayout />}>
          <Route path="users" element={<UsersPage />} />
          <Route path="roles" element={<RolesPage />} />
        </Route>
        <Route path="login" element={<LoginPage />} />
      </Route>
    </Routes>
  );
};

export const AppContainer: FC = () => {
  const settingsLogic = useInjection(ISettingsLogic.$);
  const { theme } = useValues(settingsLogic);

  return (
    <div className={`app-container theme-${themeClasses[theme]}`}>
      <Outlet />
    </div>
  );
};

export const AppLayout: FC = () => {
  const settingsLogic = useInjection(ISettingsLogic.$);

  const { sidebarType, sidebarActive, fontSize } = useValues(settingsLogic);
  const { setSidebarType, setTheme, toggleSidebar, setFontSize } =
    useActions(settingsLogic);

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
        <Button label="Light" onClick={() => setTheme(Theme.Light)} />
        <Slider
          min={6}
          max={22}
          value={fontSize}
          onChange={(e) =>
            setFontSize(typeof e.value == 'number' ? e.value : 14)
          }
        />
      </div>
      <div
        onClick={() => toggleSidebar(false)}
        className="layout-content-mask"
      />
    </div>
  );
};
