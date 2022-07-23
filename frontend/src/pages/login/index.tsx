import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import { memo } from 'react';
import { Trans, useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';

import './style.scss';

const LoginPage = memo(function LoginPage() {
  const { t } = useTranslation();

  return (
    <div id="login-page">
      <span id="login-page-title">
        <Trans>login.welcomeBack</Trans>
      </span>
      <div id="login-no-account">
        <span id="login-no-account-text">
          <Trans>login.noAccount</Trans>
        </span>
        <Link to="/register" id="login-no-account-link">
          <Trans>login.createAccount</Trans>
        </Link>
      </div>
      <label htmlFor="login-username">
        <Trans>user.username</Trans>
      </label>
      <InputText id="login-username" />

      <label htmlFor="login-password">
        <Trans>user.password</Trans>
      </label>
      <InputText id="login-password" />

      <div id="login-password-floor">
        <a href="" id="login-forgot-password">
          <Trans>login.forgot</Trans>
        </a>
      </div>

      <Button label={t('login.submit')} id="login-submit" />
    </div>
  );
});

export default LoginPage;
