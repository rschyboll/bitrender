import { useInjection } from 'inversify-react';
import { BindLogic, useValues } from 'kea';
import {
  FC,
  LazyExoticComponent,
  Suspense,
  lazy,
  startTransition,
  useCallback,
  useState,
} from 'react';
import { Outlet, Route, Routes, useNavigate } from 'react-router-dom';

import { IRouteLogic, ISettingsLogic } from '@/logic/interfaces';
import { AppPage } from '@/pages/app';
import { ErrorPage } from '@/pages/error';
import { themeClasses } from '@/types/settings';

import EntryPage from './entry';
import { ProtectedRoute } from './router';

const lazyPageFactory = (
  promise: () => Promise<{ default: FC }>,
  retry: () => void,
) =>
  lazy(async () => {
    try {
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

const BasePage: FC = () => {
  const settingsLogic = useInjection(ISettingsLogic.$);
  const { theme } = useValues(settingsLogic);

  return (
    <div style={{ height: '100%' }} className={`theme-${themeClasses[theme]}`}>
      <Outlet />
    </div>
  );
};

export const Pages: FC = () => {
  const UsersPage = useLazyPage(() => import('@/pages/users'));
  const RolesPage = useLazyPage(() => import('@/pages/roles'));
  const LoginPage = useLazyPage(() => import('@/pages/login'));
  const RegisterPage = useLazyPage(() => import('@/pages/register'));
  const RecoveryPage = useLazyPage(() => import('@/pages/recovery'));
  const VerifyPage = useLazyPage(() => import('@/pages/verify'));

  const routeLogic = useInjection(IRouteLogic.$);
  const navigate = useNavigate();

  return (
    <BindLogic logic={routeLogic} props={{ navigate: navigate }}>
      <Suspense>
        <Routes>
          <Route path="/" element={<BasePage />}>
            <Route path="app" element={<AppPage />}>
              <Route path="admin">
                <Route
                  path="users"
                  element={
                    <ProtectedRoute>
                      <UsersPage />
                    </ProtectedRoute>
                  }
                />
                <Route path="roles" element={<RolesPage />} />
              </Route>
              <Route path="settings" element={<RolesPage />} />
            </Route>

            <Route path="" element={<EntryPage />}>
              <Route path="login" element={<LoginPage />} />
              <Route path="register" element={<RegisterPage />} />
              <Route path="recovery" element={<RecoveryPage />} />
              <Route path="verify" element={<VerifyPage />} />
            </Route>

            <Route path="error" element={<>Wystąpił błąd</>} />
          </Route>
        </Routes>
      </Suspense>
    </BindLogic>
  );
};

export default Pages;
