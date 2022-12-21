import { BlockUI } from 'primereact/blockui';
import { ReactNode, memo } from 'react';

import { ErrorResponse, RequestStatus } from '@/services';

import styles from './style.module.scss';

export interface ResponseHandlerProps {
  requestStatuses: {
    status: RequestStatus;
    error?: ErrorResponse['error'] | null;
    loaded: boolean;
  }[];
  children: ReactNode;
}

export const ResponseHandler = memo(function ResponseHandler(
  props: ResponseHandlerProps,
) {
  if (
    props.requestStatuses.find(
      (requestStatus) =>
        requestStatus.status == RequestStatus.Running &&
        requestStatus.loaded == false,
    )
  ) {
    return <BlockUI blocked={true}>{props.children}</BlockUI>;
  }

  return <div>{props.children}</div>;
});

export default ResponseHandler;

const NotFoundHandler = memo(function NotFoundHandler() {
  return <div></div>;
});
