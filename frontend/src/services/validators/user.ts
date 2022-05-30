import { Permission, User } from '@/types/user';

import { JSONSchemaType, ajv } from '.';

const userSchema: JSONSchemaType<User> = {
  type: 'object',
  properties: {
    id: { type: 'string', format: 'uuid' },
    created_at: { type: 'string', format: 'timestamp' },
    modified_at: { type: 'string', format: 'timestamp' },
    email: { type: 'string', format: 'email' },
    role: { type: 'string' },
    permissions: {
      type: 'array',
      items: { type: 'string', enum: [Object.values(Permission)] },
    },
  },
  required: ['id', 'created_at', 'modified_at', 'email', 'role', 'permissions'],
  additionalProperties: false,
};

export const userValidator = ajv.compile(userSchema);
