import { BaseView } from '.';

export enum Permission {
  MANAGE_USERS = 'manage_users',
  MANAGE_ROLES = 'manage_roles',
}

export interface UserView extends BaseView {
  email: string;
  username: string;
  role: string;
  permissions: Permission[];
}

export interface UserCreate {
  email: string;
  username: string;
  password: string;
}
