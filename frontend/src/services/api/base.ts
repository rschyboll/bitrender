import { injectable } from 'inversify';
import ky, { HTTPError } from 'ky';

import Dependencies from '@/deps';
import {
  ApiErrorCodes,
  ErrorResponse,
  ServiceErrorType,
} from '@/types/service';
import { IServiceValidators } from '@/validators/interfaces';

import { IRouteLogic } from './../../logic/interfaces/route';

@injectable()
export class Service {
  protected api: typeof ky;
  protected serviceValidators: IServiceValidators;
  protected routeLogic: IRouteLogic;

  constructor() {
    this.serviceValidators = Dependencies.get(IServiceValidators.$);
    this.routeLogic = Dependencies.get(IRouteLogic.$);

    this.api = ky.create({
      prefixUrl: 'http://127.0.0.1:8001/api/app/',
      hooks: {
        beforeError: [(error) => this.onError(error)],
      },
      mode: 'cors',
      credentials: 'include',
      keepalive: true,
    });
  }

  private async onError(error: HTTPError): Promise<HTTPError> {
    const errorBody = await error.response.json();
    error.response.json = async () => errorBody;

    if (this.serviceValidators.validateHttpError(errorBody)) {
      console.log(errorBody.detail);
      switch (errorBody.detail) {
        case ApiErrorCodes.NotAuthenticated:
          console.log('HELP');
          await this.onUnauthenticatedError();
          return error;

        default:
          return error;
      }
    }
    return error;
  }

  private async onUnauthenticatedError() {
    console.log('HMM');
    this.routeLogic().actions.openLoginPage();
  }

  protected async parseAPIError(error: unknown): Promise<ErrorResponse> {
    if (error instanceof HTTPError) {
      const errorBody = await error.response.json();
      if (this.serviceValidators.validateHttpError(errorBody)) {
        return {
          success: false,
          error: {
            type: ServiceErrorType.ApiError,
            detail: errorBody.detail,
            status: error.response.status,
          },
        };
      }
      return {
        success: false,
        error: {
          type: ServiceErrorType.HTTPError,
          detail: errorBody,
          status: error.response.status,
        },
      };
    }
    return {
      success: false,
      error: {
        type: ServiceErrorType.UnknownError,
      },
    };
  }
}
