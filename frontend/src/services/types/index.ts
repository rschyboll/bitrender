import type { ApiErrorCodes, ServiceErrorType } from "../enums";

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
