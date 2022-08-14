import { useInjection } from 'inversify-react';
import { getContext, useValues } from 'kea';
import {
  FC,
  LazyExoticComponent,
  Suspense,
  lazy,
  memo,
  startTransition,
  useCallback,
  useEffect,
  useState,
} from 'react';
import { Outlet, Route, Routes, useLocation } from 'react-router-dom';

import { ISettingsLogic } from '@/logic/interfaces';
import { AppPage } from '@/pages/app';
import { ErrorPage } from '@/pages/error';
import { themeClasses } from '@/types/settings';
import { sleep } from '@/utils/async';

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

const BasePage: FC = memo(function BasePage() {
  const settingsLogic = useInjection(ISettingsLogic.$);
  const { theme } = useValues(settingsLogic);

  useEffect(() => {
    const test = async () => {
      while (true) {
        await sleep(1000);
        const context = getContext();

        console.log(context.mount.counter);
      }
    };
    test();
  }, []);

  return (
    <div style={{ height: '100%' }} className={`theme-${themeClasses[theme]}`}>
      <Outlet />
    </div>
  );
});

export const Pages: FC = memo(function Pages() {
  const UsersPage = useLazyPage(() => import('@/pages/users'));
  const RolesPage = useLazyPage(() => import('@/pages/roles'));
  const LoginPage = useLazyPage(() => import('@/pages/login'));
  const RegisterPage = useLazyPage(() => import('@/pages/register'));
  const RecoveryPage = useLazyPage(() => import('@/pages/recovery'));

  return (
    <Suspense>
      <Routes>
        <Route key="/" path="/" element={<BasePage />}>
          <Route key="app" path="app" element={<AppPage />}>
            <Route path="admin">
              <Route key="users" path="users" element={<UsersPage />} />
              <Route key="roles" path="roles" element={<RolesPage />} />
            </Route>
          </Route>

          <Route element={<EntryPage />}>
            <Route path="login" element={<LoginPage />} />
            <Route path="register" element={<RegisterPage />} />
            <Route path="recovery" element={<RecoveryPage />} />
          </Route>

          <Route path="error" element={<>Wystąpił błąd</>} />
        </Route>
      </Routes>
    </Suspense>
  );
});

export default Pages;
