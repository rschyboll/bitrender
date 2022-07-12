export enum ApiErrorCodes {
  ResourceNotFound = 'RESOURCE_NOT_FOUND',
  NotAuthenticated = 'NOT_AUTHENTICATED',
  NotAuthorized = 'NOT_AUTHORIZED',
  UserNotVerified = 'USER_NOT_VERIFIED',
  BadCredentials = 'BAD_CREDENTIALS',
  UserAlreadyExists = 'USER_ALREADY_EXISTS',
  NoDefaultRole = 'NO_DEFAULT_ROLE',
}

export interface ApiError {
  detail: ApiErrorCodes;
}
