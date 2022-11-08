import { useInjection } from "inversify-react";
import { useActions, useValues } from "kea";
import { Button } from "primereact/button";
import {
  FormEvent,
  memo,
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";
import { Trans, useTranslation } from "react-i18next";
import {
  RiEyeFill,
  RiEyeOffFill,
  RiLockFill,
  RiUserFill,
} from "react-icons/ri";

import { Link } from "@/components/link";
import { TextField } from "@/components/textField";
import { IAuthLogic } from "@/logic/interfaces";
import { ApiErrorCodes, RequestStatus } from "@/services";

import "./style.scss";

const LoginPage = memo(function LoginPage() {
  const authLogic = useInjection(IAuthLogic.$);

  const { t } = useTranslation();

  const { loginStatus, loginErrorDetail } = useValues(authLogic);
  const { login } = useActions(authLogic);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [noUsernameError, setNoUsernameError] = useState(false);
  const [noPasswordError, setNoPasswordError] = useState(false);
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [tryAgainVisible, setTryAgainVisible] = useState(false);

  const loginStatusRef = useRef(loginStatus);

  const submit = useCallback(
    async (e: FormEvent) => {
      e.preventDefault();
      if (username == "") {
        setNoUsernameError(true);
      } else {
        setNoUsernameError(false);
      }
      if (password == "") {
        setNoPasswordError(true);
      } else {
        setNoPasswordError(false);
      }
      if (username != "" && password != "") {
        login(username, password);
      }
    },
    [username, password, login]
  );

  useEffect(() => {
    loginStatusRef.current = loginStatus;
    if (loginStatus == RequestStatus.Failure) {
      setTimeout(() => {
        setTryAgainVisible(true);
      }, 3000);
    } else {
      setTryAgainVisible(false);
    }
  }, [loginStatus]);

  const togglePasswordVisibility = useCallback(() => {
    setPasswordVisible(!passwordVisible);
  }, [setPasswordVisible, passwordVisible]);

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

      <form id="login-page-form" onSubmit={submit}>
        <TextField
          id="login-username-field"
          inputId="login-username"
          value={username}
          onChange={setUsername}
          label="user.username"
          leftIcon={RiUserFill}
          errorMessage={noUsernameError ? "login.cannotBeEmpty" : undefined}
        />

        <TextField
          id="login-password-field"
          inputId="login-password"
          value={password}
          onChange={setPassword}
          label="user.password"
          type={passwordVisible ? "text" : "password"}
          leftIcon={RiLockFill}
          rightIcon={passwordVisible ? RiEyeOffFill : RiEyeFill}
          onRightIconClick={togglePasswordVisibility}
          errorMessage={noPasswordError ? "login.cannotBeEmpty" : undefined}
          floorRightContent={
            <Link to="/forgot-password" id="login-forgot-password">
              <Trans>login.forgot</Trans>
            </Link>
          }
        />

        <Button
          className={
            loginStatus == RequestStatus.Failure && !tryAgainVisible
              ? "p-button-danger"
              : ""
          }
          disabled={loginStatus == RequestStatus.Loading}
          label={
            loginStatus == RequestStatus.Loading
              ? t("login.loggingIn")
              : loginStatus == RequestStatus.Failure
              ? tryAgainVisible
                ? t("tryAgain")
                : loginErrorDetail == ApiErrorCodes.BadCredentials
                ? t("login.badCredentials")
                : t("login.unknownError")
              : t("login.submit")
          }
          id="login-submit"
          type="submit"
        />
      </form>
    </div>
  );
});

export default LoginPage;
