import type { ApiErrorCodes, ServiceErrorType } from '../enums';

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

export declare type Response<T> = SuccessResponse<T> | ErrorResponse;
