import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import { memo } from 'react';
import { Trans, useTranslation } from 'react-i18next';

import './style.scss';

const RegisterPage = memo(function RegisterPage() {
  const { t } = useTranslation();

  return (
    <div id="register-page">
      <span id="register-page-title">
        <Trans>register.createYourAccount</Trans>
      </span>
      <label htmlFor="register-username">
        <Trans>user.username</Trans>
      </label>
      <InputText id="register-username" />

      <label htmlFor="register-password">
        <Trans>user.password</Trans>
      </label>
      <InputText id="register-password" />

      <Button id="register-submit" label={t('register.submit')} />
    </div>
  );
});

export default RegisterPage;
