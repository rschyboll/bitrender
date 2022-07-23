import { BrowserHistory, Update } from 'history';
import {
  useCallback,
  useEffect,
  useLayoutEffect,
  useRef,
  useState,
  useTransition,
} from 'react';
import { Router } from 'react-router-dom';
import LoadingBar, { LoadingBarRef } from 'react-top-loading-bar';

export interface BrowserRouterProps {
  children?: React.ReactNode;
  history: BrowserHistory;
}

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
