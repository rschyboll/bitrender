import { AfterResponseHook, BeforeRequestHook } from 'ky';

declare module '@alice-health/ky-hooks-change-case' {
  const requestToSnakeCase: BeforeRequestHook;
  const responseToCamelCase: AfterResponseHook;
}
