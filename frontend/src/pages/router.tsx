import { BrowserHistory, Update } from 'history';
import { createBrowserHistory } from 'history';
import { useInjection } from 'inversify-react';
import { useValues } from 'kea';
import {
  Children,
  ReactElement,
  memo,
  useCallback,
  useEffect,
  useLayoutEffect,
  useMemo,
  useRef,
  useState,
  useTransition,
} from 'react';
import { Navigate, Router } from 'react-router-dom';
import LoadingBar, { LoadingBarRef } from 'react-top-loading-bar';

import { IAppLogic } from '@/logic/interfaces';
import { Permission } from '@/types/user';

import { LoadingPage } from './loading';

export interface BrowserRouterProps {
  children?: React.ReactNode;
  history: BrowserHistory;
}

export const history = createBrowserHistory({ window: window });

export function SuspenseRouter({ children, history }: BrowserRouterProps) {
  const [isPending, startTransition] = useTransition();
  const isPendingRef = useRef(isPending);
  const isTimeoutRef = useRef(false);

  const loadingBarRef = useRef<LoadingBarRef>(null);

  const [state, setState] = useState({
    action: history.action,
    location: history.location,
  });

  const setStateAsync = useCallback((update: Update) => {
    startTransition(() => {
      setState(update);
    });
  }, []);

  useLayoutEffect(
    () => history.listen(setStateAsync),
    [history, setStateAsync],
  );

  useEffect(() => {
    isPendingRef.current = isPending;
    if (isPending) {
      setTimeout(() => {
        if (isPendingRef.current && !isTimeoutRef.current) {
          isTimeoutRef.current = true;
          loadingBarRef.current?.continuousStart(0, 1000);
        }
      }, 100);
    } else {
      if (isTimeoutRef.current) {
        setTimeout(() => {
          loadingBarRef.current?.complete();
        }, 0);
        isTimeoutRef.current = false;
      }
    }
  }, [isPending]);

  return (
    <Router
      location={state.location}
      navigationType={state.action}
      navigator={history}
    >
      {children}
      <LoadingBar waitingTime={0} color="#ffc107" ref={loadingBarRef} />
    </Router>
  );
}

export default SuspenseRouter;

export interface ProtectedRouteProps {
  requiredPermissions?: Permission[];
  children: JSX.Element;
}

export const ProtectedRoute = memo(function ProtectedRoute(
  props: ProtectedRouteProps,
) {
  const appLogic = useInjection(IAppLogic.$);

  const { currentUser, appReady } = useValues(appLogic);

  const hasPermissions = useMemo(() => {
    if (props.requiredPermissions == null) {
      return true;
    }
    if (currentUser != null) {
      for (const permission of props.requiredPermissions) {
        if (!currentUser.permissions.includes(permission)) {
          return false;
        }
      }
      return true;
    }
    return false;
  }, [currentUser, props.requiredPermissions]);

  if (currentUser == null || !appReady) {
    return <LoadingPage />;
  }

  if (!hasPermissions) {
    return <Navigate to={'/unauthorized'} />;
  }

  return props.children;
});
