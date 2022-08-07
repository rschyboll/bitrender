import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import { Password } from 'primereact/password';
import { memo, useCallback, useEffect, useState } from 'react';
import { Trans, useTranslation } from 'react-i18next';
import {
  RiEyeLine,
  RiEyeOffLine,
  RiLockFill,
  RiMailFill,
  RiUserFill,
} from 'react-icons/ri';
import { Link } from 'react-router-dom';

import { ILoginLogic } from '@/logic/interfaces';
import { ApiErrorCodes, RequestStatus } from '@/types/service';
import { IUserValidators } from '@/validators/interfaces';

import './style.scss';

const RegisterPage = memo(function RegisterPage() {
  const userValidators = useInjection(IUserValidators.$);
  const loginLogic = useInjection(ILoginLogic.$);

  const {
    registerWeakPassword,
    registerWrongEmail,
    registerStatus,
    registerErrorDetail,
  } = useValues(loginLogic);
  const { register, checkLoggedIn } = useActions(loginLogic);

  const { t } = useTranslation();

  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [passwordVisible, setPasswordVisible] = useState(false);

  const [noEmailError, setNoEmailError] = useState(false);
  const [noUsernameError, setNoUsernameError] = useState(false);
  const [noPasswordError, setNoPasswordError] = useState(false);
  const [tryAgainVisible, setTryAgainVisible] = useState(false);

  const submit = useCallback(() => {
    if (email == '') {
      setNoEmailError(true);
    } else {
      setNoEmailError(false);
    }
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
    if (email != '' && username != '' && password != '') {
      register(email, username, password);
    }
  }, [email, password, register, username]);

  useEffect(() => {
    const passwordInput =
      document.getElementById('register-password')?.firstChild;
    if (passwordInput instanceof HTMLInputElement) {
      if (passwordVisible) {
        passwordInput.type = 'text';
      } else {
        passwordInput.type = 'password';
      }
    }
  }, [passwordVisible]);

  useEffect(() => {
    checkLoggedIn();
  }, [checkLoggedIn]);

  return (
    <div id="register-page">
      <span id="register-page-title">
        <Trans>register.createYourAccount</Trans>
      </span>

      <div id="register-have-account">
        <span id="register-have-account-text">
          <Trans>register.haveAccount</Trans>
        </span>
        <Link to="/login" id="register-have-account-link">
          <Trans>register.login</Trans>
        </Link>
      </div>
      <form
        id="register-form"
        onSubmit={(e) => {
          e.preventDefault();
          submit();
        }}
      >
        <div id="register-email-field" className="field">
          <label htmlFor="register-email">
            <Trans>user.email</Trans>
          </label>
          <span className="p-input-icon-left">
            <RiMailFill className="register-field-icon" />
            <InputText
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              id="register-email"
              className={
                noEmailError || registerWrongEmail ? 'p-invalid' : undefined
              }
            />
          </span>
          <small className="p-error register-field-error-text">
            <Trans>
              {noEmailError
                ? 'register.cannotBeEmpty'
                : registerWrongEmail
                ? 'register.wrongEmail'
                : registerErrorDetail == ApiErrorCodes.EmailTaken
                ? 'register.emailTaken'
                : ''}
            </Trans>
          </small>
        </div>

        <div id="register-username-field" className="field">
          <label htmlFor="register-username">
            <Trans>user.username</Trans>
          </label>
          <span className="p-input-icon-left">
            <RiUserFill className="register-field-icon" />
            <InputText
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              id="register-username"
              className={noUsernameError ? 'p-invalid' : undefined}
            />
          </span>
          <small className="p-error register-field-error-text">
            <Trans>
              {noUsernameError
                ? 'register.cannotBeEmpty'
                : registerErrorDetail == ApiErrorCodes.UsernameTaken
                ? 'register.usernameTaken'
                : ''}
            </Trans>
          </small>
        </div>

        <div id="register-password-field" className="field">
          <label htmlFor="register-password">
            <Trans>user.password</Trans>
          </label>
          <span className="p-input-icon-left p-input-icon-right">
            <RiLockFill className="register-field-icon" />
            <Password
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              id="register-password"
              mediumRegex={userValidators.mediumPasswordRegExp.source}
              strongRegex={userValidators.strongPasswordRegExp.source}
              className={
                registerWeakPassword || noPasswordError
                  ? 'p-invalid'
                  : undefined
              }
            />
            {passwordVisible ? (
              <RiEyeOffLine
                id="register-password-view-button"
                onClick={() => setPasswordVisible(false)}
                className="register-field-icon"
              />
            ) : (
              <RiEyeLine
                id="register-password-view-button"
                onClick={() => setPasswordVisible(true)}
                className="register-field-icon"
              />
            )}
          </span>
          <small className="p-error register-field-error-text">
            <Trans>
              {noPasswordError
                ? 'register.cannotBeEmpty'
                : registerWeakPassword
                ? 'register.weakPassword'
                : ''}
            </Trans>
          </small>
        </div>

        <Button
          className={
            registerStatus == RequestStatus.Error && !tryAgainVisible
              ? 'p-button-danger'
              : ''
          }
          disabled={registerStatus == RequestStatus.Loading}
          label={
            registerStatus == RequestStatus.Loading
              ? t('register.inProcess')
              : registerStatus == RequestStatus.Error
              ? tryAgainVisible
                ? t('tryAgain')
                : t('register.unknownError')
              : t('register.submit')
          }
          id="register-submit"
          type="submit"
        />
      </form>
    </div>
  );
});

export default RegisterPage;
