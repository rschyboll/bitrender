import { MRole } from '@/types/models';

import { IRoleValidators } from '../interfaces';
import { JSONSchemaType, ValidateFunction, Validators } from './base';

export class RoleValidators extends Validators implements IRoleValidators {
  viewSchema: JSONSchemaType<MRole.View> = {
    type: 'object',
    properties: {
      id: { type: 'string' },
      createdAt: { type: 'string' },
      modifiedAt: { type: 'string' },
      name: { type: 'string' },
      default: { type: 'boolean', nullable: true, enum: [true, null] },
      permissions: {
        type: 'array',
        items: { type: 'string', enum: Object.values(MRole.Permission) },
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
  };
  createSchema = this.viewSchema;
  getRolesOutputSchema: JSONSchemaType<MRole.Messages.GetListOutput> = {
    type: 'object',
    properties: {
      items: {
        type: 'array',
        items: this.viewSchema,
      },
      rowCount: {
        type: 'integer',
      },
    },
    required: ['rowCount', 'items'],
  };
  createOutputValidator: ValidateFunction<MRole.Messages.CreateOutput>;
  getRolesOutputValidator: ValidateFunction<MRole.Messages.GetListOutput>;
  getByIdOutputValidator: ValidateFunction<MRole.Messages.GetByIdOutput>;

  constructor() {
    super();
    this.createOutputValidator = this.ajv.compile(this.createSchema);
    this.getRolesOutputValidator = this.ajv.compile(this.getRolesOutputSchema);
    this.getByIdOutputValidator = this.ajv.compile(this.viewSchema);
  }

  public validateGetListOutput(
    value: unknown,
  ): value is MRole.Messages.GetListOutput {
    return this.getRolesOutputValidator(value);
  }

  public validateCreateOutput(
    value: unknown,
  ): value is MRole.Messages.CreateOutput {
    return this.createOutputValidator(value);
  }

  public validateGetByIdOutput(value: unknown): value is MRole.View {
    return this.getByIdOutputValidator(value);
  }

  public isPermission(value: unknown): value is MRole.Permission {
    return (
      typeof value == 'string' &&
      Object.values(MRole.Permission).includes(value as MRole.Permission)
    );
  }
}
