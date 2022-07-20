import {
  FC,
  Suspense,
  lazy,
  memo,
  useCallback,
  useMemo,
  useState,
} from 'react';

interface LazyLoaderProps {
  promise: () => Promise<{ default: FC }>;
  fallback: FC<{ retry: () => void }>;
}

const LazyLoader = memo(function LazyLoader(props: LazyLoaderProps) {
  const [retry, setRetry] = useState(true);

  const retryLoading = useCallback(() => {
    setRetry(!retry);
  }, [retry, setRetry]);

  const Lazy = useMemo(() => {
    const test = lazy(async () => {
      try {
        const test = await props.promise();
        return test;
      } catch {
        return { default: () => <props.fallback retry={retryLoading} /> };
      }
    });

    return test;
  }, []);

  return (
    <Suspense fallback={'HELP'}>
      <Lazy />
    </Suspense>
  );
});

export default LazyLoader;
