import { injectable } from 'inversify';
import ky, { HTTPError } from 'ky';

import Dependencies from '@/deps';
import { IAppLogic } from '@/logic/interfaces';
import { ErrorResponse, ServiceErrorType } from '@/types/service';
import { IServiceValidators } from '@/validators/interfaces';

@injectable()
export class Service {
  protected api: typeof ky;
  protected serviceValidators: IServiceValidators;
  protected appLogic: IAppLogic;

  constructor() {
    this.serviceValidators = Dependencies.get(IServiceValidators.$);
    this.appLogic = Dependencies.get(IAppLogic.$);

    this.api = ky.create({
      prefixUrl: 'http://127.0.0.1:8001/api/app/',
      hooks: {
        beforeError: [
          async (error) => {
            const errorBody = await error.response.json();
            this.appLogic.actions.openLoginPage();
            return error;
          },
        ],
      },
    });
  }

  protected async parseAPIError(error: unknown): Promise<ErrorResponse> {
    if (error instanceof HTTPError) {
      const errorBody = await error.response.json();
      if (this.serviceValidators.validateHttpError(errorBody)) {
        return {
          success: false,
          error: {
            type: ServiceErrorType.HTTPError,
            detail: errorBody.detail,
            status: error.response.status,
          },
        };
      }
      return {
        success: false,
        error: {
          type: ServiceErrorType.HTTPError,
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
