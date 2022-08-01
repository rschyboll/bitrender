import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import { memo, useCallback, useEffect, useRef, useState } from 'react';
import { Trans, useTranslation } from 'react-i18next';
import {
  RiEyeLine,
  RiEyeOffLine,
  RiLockFill,
  RiUserFill,
} from 'react-icons/ri';
import { Link } from 'react-router-dom';

import { ILoginLogic } from '@/logic/interfaces';
import { ApiErrorCodes, RequestStatus } from '@/types/service';

import './style.scss';

const LoginPage = memo(function LoginPage() {
  const loginLogic = useInjection(ILoginLogic.$);

  const { t } = useTranslation();

  const { loginStatus, loginErrorDetail } = useValues(loginLogic);
  const { login } = useActions(loginLogic);

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [noUsernameError, setNoUsernameError] = useState(false);
  const [noPasswordError, setNoPasswordError] = useState(false);
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [tryAgainVisible, setTryAgainVisible] = useState(false);

  const loginStatusRef = useRef(loginStatus);

  const submit = useCallback(async () => {
    if (username == '') {
      setNoUsernameError(true);
    } else {
      setNoUsernameError(false);
    }
    if (password == '') {
      setNoPasswordError(true);
    } else {
      setNoPasswordError(false);
    }
    if (username != '' && password != '') {
      login(username, password);
    }
  }, [username, password, login]);

  useEffect(() => {
    loginStatusRef.current = loginStatus;
    if (loginStatus == RequestStatus.Error) {
      setTimeout(() => {
        setTryAgainVisible(true);
      }, 3000);
    } else {
      setTryAgainVisible(false);
    }
  }, [loginStatus]);

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
      <div id="login-username-field" className="field">
        <label htmlFor="login-username">
          <Trans>user.username</Trans>
        </label>
        <span className="p-input-icon-left">
          <RiUserFill className="login-field-icon" />
          <InputText
            id="login-username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className={noUsernameError ? 'p-invalid' : undefined}
          />
        </span>
        <small className="p-error login-field-error-text">
          {noUsernameError ? <Trans>login.cannotBeEmpty</Trans> : ''}
        </small>
      </div>

      <div id="login-password-field" className="field">
        <label htmlFor="login-password">
          <Trans>user.password</Trans>
        </label>
        <span className="p-input-icon-left p-input-icon-right">
          <RiLockFill className="login-field-icon" />
          <InputText
            id="login-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type={passwordVisible ? 'text' : 'password'}
            className={noPasswordError ? 'p-invalid' : undefined}
          />
          {passwordVisible ? (
            <RiEyeLine
              id="login-password-view-button"
              onClick={() => setPasswordVisible(false)}
              className="login-field-icon"
            />
          ) : (
            <RiEyeOffLine
              id="login-password-view-button"
              onClick={() => setPasswordVisible(true)}
              className="login-field-icon"
            />
          )}
        </span>
      </div>

      <div id="login-password-floor">
        <a href="" id="login-forgot-password">
          <Trans>login.forgot</Trans>
        </a>
        <small className="p-error">
          {noPasswordError ? <Trans>login.cannotBeEmpty</Trans> : ''}
        </small>
      </div>

      <Button
        className={
          loginStatus == RequestStatus.Error && !tryAgainVisible
            ? 'p-button-danger'
            : ''
        }
        disabled={loginStatus == RequestStatus.Loading}
        label={
          loginStatus == RequestStatus.Loading
            ? t('login.loggingIn')
            : loginStatus == RequestStatus.Error
            ? tryAgainVisible
              ? t('tryAgain')
              : loginErrorDetail == ApiErrorCodes.BadCredentials
              ? t('login.badCredentials')
              : t('login.unknownError')
            : t('login.submit')
        }
        id="login-submit"
        onClick={submit}
      />
    </div>
  );
});

export default LoginPage;
