import { ApiError, ApiErrorCodes } from '@/types/service';
import { IServiceValidators } from '@/validators/interfaces';

import { JSONSchemaType, ValidateFunction, Validators } from '.';

export class ServiceValidators
  extends Validators
  implements IServiceValidators
{
  apiErrorSchema: JSONSchemaType<ApiError> = {
    type: 'object',
    properties: {
      detail: { type: 'string', enum: Object.values(ApiErrorCodes) },
    },
    required: ['detail'],
  };
  apiErrorValidator: ValidateFunction<ApiError>;

  constructor() {
    super();
    this.apiErrorValidator = this.ajv.compile(this.apiErrorSchema);
  }

  public validateHttpError(response: unknown): response is ApiError {
    return this.apiErrorValidator(response);
  }
}
