import { injectable } from 'inversify';
import ky, { HTTPError } from 'ky';

import { IUtilityConverters } from '@/converters/interfaces';
import Dependencies from '@/deps';
import { IRouteLogic } from '@/logic/interfaces/route';
import { ApiErrorCodes, ErrorResponse, ServiceErrorType } from '@/services';
import { IServiceValidators } from '@/validators/interfaces';

import { ListRequestInput } from '../messages/list';

@injectable()
export class Service {
  protected api: typeof ky;
  protected utilityConverters: IUtilityConverters;
  protected serviceValidators: IServiceValidators;
  protected routeLogic: IRouteLogic;

  constructor() {
    this.utilityConverters = Dependencies.get(IUtilityConverters.$);
    this.serviceValidators = Dependencies.get(IServiceValidators.$);
    this.routeLogic = Dependencies.get(IRouteLogic.$);

    this.api = ky.create({
      prefixUrl: 'http://127.0.0.1:8123/api/app/',
      hooks: {
        beforeError: [(error) => this.onError(error)],
        beforeRequest: [
          (request, options) =>
            this.utilityConverters.requestToSnakeCase(request, options),
        ],
        afterResponse: [
          (request, options, response) =>
            this.utilityConverters.responseToCamelCase(
              request,
              options,
              response,
            ),
        ],
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
      switch (errorBody.detail) {
        case ApiErrorCodes.NotAuthenticated:
          await this.onUnauthenticatedError();
          return error;

        default:
          return error;
      }
    }
    return error;
  }

  private async onUnauthenticatedError() {
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

  protected listRequestToURL(input: ListRequestInput<string>): URLSearchParams {
    const { page, search, sort } = input;

    const searchParams = new URLSearchParams();

    if (page != null) {
      searchParams.append('page_nr', page.pageNr.toString());
      searchParams.append('records_per_page', page.recordsPerPage.toString());
    }

    if (sort != null) {
      searchParams.append('column', sort.column);
      searchParams.append('order', sort.order.toString());
    }

    for (const searchItem of search) {
      searchParams.append('search_column', searchItem.column);
      searchParams.append('search_rule', searchItem.rule.toString());
      searchParams.append(
        'search_value',
        searchItem.value != null ? searchItem.value.toString() : '',
      );
    }

    return searchParams;
  }
}
