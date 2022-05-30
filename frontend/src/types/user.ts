import { Base } from './base';

export interface User extends Base {
  email: string;
  role: string;
  permissions: Permission[];
}

export enum Permission {
  MANAGE_USERS = 'manage_users',
  MANAGE_ROLES = 'manage_roles',
}
