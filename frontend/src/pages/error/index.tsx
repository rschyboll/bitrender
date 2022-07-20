import { Button } from 'primereact/button';
import { memo, useCallback, useTransition } from 'react';

import { history } from '@/pages/history';

export interface ErrorPageProps {
  retry?: () => void;
}

export const ErrorPage = memo(function ErrorPage(props: ErrorPageProps) {
  return <Button onClick={props.retry} label="RETRY" />;
});
