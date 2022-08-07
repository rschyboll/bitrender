export enum ApiErrorCodes {
  ResourceNotFound = 'RESOURCE_NOT_FOUND',
  NotAuthenticated = 'NOT_AUTHENTICATED',
  NotAuthorized = 'NOT_AUTHORIZED',
  UserNotVerified = 'USER_NOT_VERIFIED',
  BadCredentials = 'BAD_CREDENTIALS',
  EmailTaken = 'EMAIL_TAKEN',
  UsernameTaken = 'USERNAME_TAKEN',
  NoDefaultRole = 'NO_DEFAULT_ROLE',
}

export enum ServiceErrorType {
  ApiError = 'API_ERROR',
  HTTPError = 'HTTP_ERROR',
  ValidationError = 'VALIDATION_ERROR',
  UnknownError = 'UNKNOWN_ERROR',
}

export interface ApiError {
  detail: ApiErrorCodes;
}

export declare type SuccessResponse<T> = {
  success: true;
  data: T;
};

export declare type ErrorResponse = {
  success: false;
  error:
    | {
        type: ServiceErrorType.ApiError;
        detail: ApiErrorCodes;
        status: number;
      }
    | {
        type: ServiceErrorType.HTTPError;
        detail: unknown;
        status: number;
      }
    | {
        type: ServiceErrorType.ValidationError | ServiceErrorType.UnknownError;
      };
};

export declare type UnknownResponse<T> = {
  success: never;
  data?: T;
  error?: {
    type: ServiceErrorType;
    status?: number;
    detail?: ApiErrorCodes;
  };
};

export declare type Response<T> =
  | UnknownResponse<T>
  | SuccessResponse<T>
  | ErrorResponse;

export enum RequestStatus {
  Idle,
  Loading,
  Error,
  Success,
}
