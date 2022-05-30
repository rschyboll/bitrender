import { Base } from './base';

interface User extends Base {
  email: string;
  role: string;
  permissions: Permission[];
}

enum Permission {
  MANAGE_USERS = 'manage_users',
  MANAGE_ROLES = 'manage_roles',
}
