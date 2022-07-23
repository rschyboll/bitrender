import { Button } from 'primereact/button';
import { memo, useCallback, useEffect, useRef, useTransition } from 'react';
import LoadingBar, { LoadingBarRef } from 'react-top-loading-bar';

export interface ErrorPageProps {
  retry?: () => void;
}

export const ErrorPage = memo(function ErrorPage(props: ErrorPageProps) {
  const [isPending, startTransition] = useTransition();
  const loadingBarRef = useRef<LoadingBarRef>(null);
  const isPendingRef = useRef(isPending);
  const isTimeoutRef = useRef(false);

  const retry = useCallback(() => {
    if (props.retry != null) {
      startTransition(() => {
        if (props.retry != null) props.retry();
      });
    }
  }, [props]);

  useEffect(() => {
    if (isPending) {
      setTimeout(() => {
        if (isPendingRef.current) {
          isTimeoutRef.current = true;
          loadingBarRef.current?.continuousStart(0, 1000);
        }
      }, 50);
    } else {
      if (isTimeoutRef.current) {
        loadingBarRef.current?.complete();
        isTimeoutRef.current = false;
      }
    }
    isPendingRef.current = isPending;
  }, [isPending]);

  return (
    <>
      <LoadingBar waitingTime={0} color="#ffc107" ref={loadingBarRef} />
      <Button disabled={isPending} onClick={retry} label="RETRY" />
    </>
  );
});
