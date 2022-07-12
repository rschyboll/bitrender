import { Permission, UserViewResponse } from '@/types/user';

import { JSONSchemaType, ValidateFunction, Validators } from '.';
import { IUserValidators } from '../interfaces';

export class UserValidators extends Validators implements IUserValidators {
  userViewResponseSchema: JSONSchemaType<UserViewResponse> = {
    type: 'object',
    properties: {
      id: { type: 'string', format: 'uuid' },
      created_at: { type: 'string', format: 'timestamp' },
      modified_at: { type: 'string', format: 'timestamp' },
      email: { type: 'string', format: 'email' },
      role: { type: 'string' },
      permissions: {
        type: 'array',
        items: { type: 'string', enum: Object.values(Permission) },
      },
    },
    required: [
      'id',
      'created_at',
      'modified_at',
      'email',
      'role',
      'permissions',
    ],
  };
  userViewResponseValidator: ValidateFunction<UserViewResponse>;

  constructor() {
    super();
    this.userViewResponseValidator = this.ajv.compile(
      this.userViewResponseSchema,
    );
  }

  public validateUserViewResponse(
    response: unknown,
  ): response is UserViewResponse {
    return this.userViewResponseValidator(response);
  }
}
