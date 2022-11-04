import { memo } from 'react';
import { Trans } from 'react-i18next';

import './style.scss';

export const LoadingPage = memo(function LoadingPage() {
  return (
    <>
      <span className="loader-text">
        <Trans>loading</Trans>...
      </span>
      <div className="loader">
        <span className="loader-block"></span>
        <span className="loader-block"></span>
        <span className="loader-block"></span>
        <span className="loader-block"></span>
        <span className="loader-block"></span>
        <span className="loader-block"></span>
        <span className="loader-block"></span>
        <span className="loader-block"></span>
        <span className="loader-block"></span>
      </div>
    </>
  );
});
