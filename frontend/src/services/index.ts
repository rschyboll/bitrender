export declare type SuccessResponse<T> = {
  success: true;
  data: T;
  error?: {
    detail?: string;
  };
};

export declare type ErrorResponse = {
  success: false;
  data?: undefined;
  error: {
    detail: string;
  };
};

export declare type UnknownResponse<T> = {
  success: never;
  data?: T;
  error?: {
    detail?: string;
  };
};

export declare type Response<T> =
  | UnknownResponse<T>
  | SuccessResponse<T>
  | ErrorResponse;
