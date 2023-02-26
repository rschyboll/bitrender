import { Permission } from '@/schemas/role';
import { GetRolesOutput } from '@/services/messages/role';

import { IRoleValidators } from '../interfaces';
import { JSONSchemaType, ValidateFunction, Validators } from './base';

export class RoleValidators extends Validators implements IRoleValidators {
  getRolesOutputSchema: JSONSchemaType<GetRolesOutput> = {
    type: 'object',
    properties: {
      items: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            id: { type: 'string' },
            createdAt: { type: 'string' },
            modifiedAt: { type: 'string' },
            name: { type: 'string' },
            default: { type: 'boolean', nullable: true, enum: [true, null] },
            permissions: {
              type: 'array',
              items: { type: 'string', enum: Object.values(Permission) },
            },
          },
          required: [
            'id',
            'createdAt',
            'modifiedAt',
            'default',
            'name',
            'permissions',
          ],
        },
      },
      rowCount: {
        type: 'integer',
      },
    },
    required: ['rowCount', 'items'],
  };
  getRolesOutputValidator: ValidateFunction<GetRolesOutput>;

  constructor() {
    super();
    this.getRolesOutputValidator = this.ajv.compile(this.getRolesOutputSchema);
  }

  public validateGetRolesOutput(value: unknown): value is GetRolesOutput {
    console.log(value);
    console.log(this.getRolesOutputValidator.errors);
    return this.getRolesOutputValidator(value);
  }
}
