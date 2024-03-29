export enum ApiErrorCodes {
  ResourceNotFound = 'RESOURCE_NOT_FOUND',
  NotAuthenticated = 'NOT_AUTHENTICATED',
  NotAuthorized = 'NOT_AUTHORIZED',
  UserNotVerified = 'USER_NOT_VERIFIED',
  BadCredentials = 'BAD_CREDENTIALS',
  EmailTaken = 'EMAIL_TAKEN',
  UsernameTaken = 'USERNAME_TAKEN',
  NoDefaultRole = 'NO_DEFAULT_ROLE',
  RoleNameTaken = 'ROLE_NAME_TAKEN',
}

export enum ServiceErrorType {
  ApiError = 'API_ERROR',
  HTTPError = 'HTTP_ERROR',
  ValidationError = 'VALIDATION_ERROR',
  UnknownError = 'UNKNOWN_ERROR',
}

export enum RequestStatus {
  Idle = 'idle',
  Running = 'running',
  Success = 'success',
  Failure = 'failure',
}

export enum StreamStatus {
  Connecting = 'Connecting',
  Open = 'Open',
  Closing = 'Closing',
  Closed = 'Closed',
}
