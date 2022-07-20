import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Button } from 'primereact/button';
import { Slider } from 'primereact/slider';
import {
  FC,
  LazyExoticComponent,
  Suspense,
  lazy,
  startTransition,
  useCallback,
  useState,
} from 'react';
import { Link, Outlet, Route, Routes, useLocation } from 'react-router-dom';

import { Sidebar } from '@/components/sidebar';
import { Topbar } from '@/components/topbar';
import { IAppLogic, ISettingsLogic } from '@/logic/interfaces';
import { ErrorPage } from '@/pages/error';
import {
  SidebarType,
  Theme,
  layoutTypesClasses,
  themeClasses,
} from '@/types/settings';

import './style.scss';

const verticalTypes = [SidebarType.Static, SidebarType.Slim];

const LoginPage = lazy(() => import('@/pages/login'));
const RegisterPage = lazy(() => import('@/pages/register'));
const RecoveryPage = lazy(() => import('@/pages/recovery'));
const RolesPage = lazy(async () => {
  return import('@/pages/roles');
});
const usersPageFactory = (retry: () => void) =>
  lazy(async () => {
    try {
      await new Promise((r) => setTimeout(r, 500));
      return await import('@/pages/users');
    } catch (error) {
      return { default: () => <ErrorPage retry={retry} /> };
    }
  });

export const App: FC = () => {
  const usersPageRetry = useCallback(() => {
    startTransition(() => {
      setUsersPage(usersPageFactory(usersPageRetry));
    });
  }, []);

  const [UsersPage, setUsersPage] = useState<LazyExoticComponent<any>>(
    usersPageFactory(usersPageRetry),
  );

  return (
    <Suspense>
      <Routes>
        <Route path="/" element={<AppContainer />}>
          <Route path="app" element={<AppLayout />}>
            <Route path="users" element={<UsersPage />} />
            <Route path="roles" element={<RolesPage />} />
          </Route>
          <Route path="login" element={<LoginPage />} />
          <Route path="register" element={<RegisterPage />} />
          <Route path="recovery" element={<RecoveryPage />} />
          <Route path="error" element={<>Wystąpił błąd</>} />
        </Route>
      </Routes>
    </Suspense>
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
  const appLogic = useInjection(IAppLogic.$);

  const { sidebarType, sidebarActive, fontSize } = useValues(settingsLogic);
  const { setSidebarType, setTheme, toggleSidebar, setFontSize } =
    useActions(settingsLogic);
  const { openUsersPage, openRolesPage } = useActions(appLogic);

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
        <div>
          <Button label="Roles" onClick={openRolesPage} />
          <Button label="Users" onClick={openUsersPage} />
          <Link to="/app/users">Users</Link> <Link to="/app/roles">Roles</Link>
        </div>
      </div>
      <div
        onClick={() => toggleSidebar(false)}
        className="layout-content-mask"
      />
    </div>
  );
};

export const AppPageLoading = () => {
  return <div>LOADING</div>;
};
