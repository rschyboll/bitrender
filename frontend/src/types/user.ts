import { BaseView, BaseViewResponse } from '.';

export enum Permission {
  MANAGE_USERS = 'manage_users',
  MANAGE_ROLES = 'manage_roles',
}

export interface UserViewResponse extends BaseViewResponse {
  email: string;
  role: string;
  permissions: Permission[];
}

export interface UserView extends BaseView {
  email: string;
  role: string;
  permissions: Permission[];
}
