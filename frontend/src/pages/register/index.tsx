import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Button } from 'primereact/button';
import { memo, useCallback, useEffect, useRef, useState } from 'react';
import { Trans, useTranslation } from 'react-i18next';
import { RiMailFill, RiUserFill } from 'react-icons/ri';

import { Link } from '@/components/link';
import { PasswordField } from '@/components/passwordField';
import { TextField } from '@/components/textField';
import { IAuthLogic } from '@/logic/interfaces';
import { ApiErrorCodes, RequestStatus } from '@/services';
import { IUserValidators } from '@/validators/interfaces';

import './style.scss';

const RegisterPage = memo(function RegisterPage() {
  const userValidators = useInjection(IUserValidators.$);
  const authLogic = useInjection(IAuthLogic.$);

  const {
    registerWeakPassword,
    registerWrongEmail,
    registerStatus,
    registerErrorDetail,
  } = useValues(authLogic);
  const { register } = useActions(authLogic);

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
    registerStatusRef.current = registerStatus;
    if (registerStatus == RequestStatus.Failure) {
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
            registerStatus == RequestStatus.Failure && !tryAgainVisible
              ? 'p-button-danger'
              : ''
          }
          disabled={registerStatus == RequestStatus.Running}
          label={
            registerStatus == RequestStatus.Running
              ? t('register.inProcess')
              : registerStatus == RequestStatus.Failure
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
