import { Permission, UserViewResponse } from '@/types/user';

import { IUserValidators } from '../interfaces';
import { JSONSchemaType, ValidateFunction, Validators } from './base';

export class UserValidators extends Validators implements IUserValidators {
  userViewResponseSchema: JSONSchemaType<UserViewResponse> = {
    type: 'object',
    properties: {
      id: { type: 'string', format: 'uuid' },
      created_at: { type: 'string', format: 'date' },
      modified_at: { type: 'string', format: 'date' },
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
