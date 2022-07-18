import { Button } from 'primereact/button';
import { Card } from 'primereact/card';
import { InputText } from 'primereact/inputtext';
import { FC } from 'react';
import { Trans, useTranslation } from 'react-i18next';

import { Logo } from '@/components/logo';

import './style.scss';

export const LoginPage: FC = () => {
  const { t } = useTranslation();

  return (
    <Card id="login-card" className="shadow-2">
      <Logo titleVisible={true} />
      <span id="login-card-title">
        <Trans>login.welcomeBack</Trans>
      </span>
      <div id="login-no-account">
        <span id="login-no-account-text">
          <Trans>login.noAccount</Trans>
        </span>
        <a href="" id="login-no-account-link">
          <Trans>login.createAccount</Trans>
        </a>
      </div>
      <label htmlFor="login-username">
        <Trans>login.username</Trans>
      </label>
      <InputText id="login-username" />

      <label htmlFor="login-password">
        <Trans>login.password</Trans>
      </label>
      <InputText id="login-password" />

      <div id="login-password-floor">
        <a href="" id="login-forgot-password">
          <Trans>login.forgot</Trans>
        </a>
      </div>

      <Button label={t('login.submit')} id="login-submit" />
    </Card>
  );
};
