import { memo } from 'react';
import { Trans } from 'react-i18next';

import './style.scss';

const VerifyPage = memo(function VerifyPage() {
  return (
    <div id="verify-page">
      <span id="verify-page-title">
        <Trans>verify.account</Trans>
      </span>
    </div>
  );
});

export default VerifyPage;
