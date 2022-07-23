import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import {
  FC,
  LazyExoticComponent,
  Suspense,
  lazy,
  startTransition,
  useCallback,
  useState,
} from 'react';
import { Outlet, Route, Routes } from 'react-router-dom';

import { Sidebar } from '@/components/sidebar';
import { Topbar } from '@/components/topbar';
import { ISettingsLogic } from '@/logic/interfaces';
import { ErrorPage } from '@/pages/error';
import {
  SidebarType,
  layoutTypesClasses,
  themeClasses,
} from '@/types/settings';

import './style.scss';

const verticalTypes = [SidebarType.Static, SidebarType.Slim];

const lazyPageFactory = (
  promise: () => Promise<{ default: FC }>,
  retry: () => void,
) =>
  lazy(async () => {
    try {
      await new Promise((r) => setTimeout(r, 2000));

      return await promise();
    } catch (error) {
      return { default: () => <ErrorPage retry={retry} /> };
    }
  });

const useLazyPage = (promise: () => Promise<{ default: FC }>) => {
  const pageRetry = useCallback(() => {
    startTransition(() => {
      setPage(lazyPageFactory(promise, pageRetry));
    });
  }, [promise]);

  const [page, setPage] = useState<LazyExoticComponent<FC>>(
    lazyPageFactory(promise, pageRetry),
  );

  return page;
};

export const App: FC = () => {
  const UsersPage = useLazyPage(() => import('@/pages/users'));
  const RolesPage = useLazyPage(() => import('@/pages/roles'));
  const LoginPage = useLazyPage(() => import('@/pages/login'));
  const RegisterPage = useLazyPage(() => import('@/pages/register'));
  const RecoveryPage = useLazyPage(() => import('@/pages/recovery'));

  return (
    <Suspense>
      <Routes>
        <Route path="/" element={<AppContainer />}>
          <Route path="app" element={<AppLayout />}>
            <Route path="" element={<>Test</>} />
            <Route path="admin">
              <Route path="users" element={<UsersPage />} />
              <Route path="roles" element={<RolesPage />} />
            </Route>

            <Route path="settings" element={<RolesPage />} />
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
