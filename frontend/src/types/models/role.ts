import type { MBase } from '.';

export * as Messages from '../messages/role';

export enum Permission {
  MANAGE_USERS = 'manage_users',
  MANAGE_ROLES = 'manage_roles',
}

export interface View extends MBase.View {
  name: string;
  default: true | null;
  permissions: Permission[];
}

export interface Create {
  name: string;
  default: true | null;
  permissions: Permission[];
}

export interface Update {
  name?: string;
}

export type TableView = {
  id: string;
  name: string;
  default: true | null;
} & { [Key in Permission]: boolean };

export type Columns = MBase.Columns | 'name' | 'default';
