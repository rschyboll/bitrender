import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import { Password } from 'primereact/password';
import { memo, useCallback, useEffect, useRef, useState } from 'react';
import { Trans, useTranslation } from 'react-i18next';
import {
  RiEyeLine,
  RiEyeOffLine,
  RiLockFill,
  RiMailFill,
  RiUserFill,
} from 'react-icons/ri';
import { Link } from 'react-router-dom';

import { PasswordField } from '@/components/passwordField';
import { TextField } from '@/components/textField';
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

  const [noEmailError, setNoEmailError] = useState(false);
  const [noUsernameError, setNoUsernameError] = useState(false);
  const [noPasswordError, setNoPasswordError] = useState(false);
  const [tryAgainVisible, setTryAgainVisible] = useState(false);

  const registerStatusRef = useRef(registerStatus);

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
    checkLoggedIn();
  }, [checkLoggedIn]);

  useEffect(() => {
    registerStatusRef.current = registerStatus;
    if (registerStatus == RequestStatus.Error) {
      setTimeout(() => {
        setTryAgainVisible(true);
      }, 3000);
    } else {
      setTryAgainVisible(false);
    }
  }, [registerStatus]);

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
        <TextField
          id="register-username-field"
          inputId="register-username"
          value={username}
          onChange={setUsername}
          label="user.username"
          leftIcon={RiUserFill}
          errorMessage={noUsernameError ? 'login.cannotBeEmpty' : undefined}
        />

        <TextField
          id="register-email-field"
          inputId="register-email"
          value={email}
          onChange={setEmail}
          label="user.email"
          leftIcon={RiMailFill}
          errorMessage={
            noEmailError
              ? 'register.cannotBeEmpty'
              : registerWrongEmail
              ? 'register.wrongEmail'
              : registerErrorDetail == ApiErrorCodes.EmailTaken
              ? 'register.emailTaken'
              : undefined
          }
        />

        <PasswordField
          id="register-password-field"
          inputId="register-password"
          value={password}
          onChange={setPassword}
          label="user.password"
          mediumRegex={userValidators.mediumPasswordRegExp.source}
          strongRegex={userValidators.strongPasswordRegExp.source}
          errorMessage={
            noPasswordError
              ? 'register.cannotBeEmpty'
              : registerWeakPassword
              ? 'register.weakPassword'
              : undefined
          }
        />

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
