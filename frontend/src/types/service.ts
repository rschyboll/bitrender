export enum ApiErrorCodes {
  ResourceNotFound = 'RESOURCE_NOT_FOUND',
  NotAuthenticated = 'NOT_AUTHENTICATED',
  NotAuthorized = 'NOT_AUTHORIZED',
  UserNotVerified = 'USER_NOT_VERIFIED',
  BadCredentials = 'BAD_CREDENTIALS',
  UserAlreadyExists = 'USER_ALREADY_EXISTS',
  NoDefaultRole = 'NO_DEFAULT_ROLE',
}

export enum ServiceErrorType {
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
        type: ServiceErrorType.HTTPError;
        detail?: ApiErrorCodes;
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
