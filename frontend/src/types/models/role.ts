import type { MBase } from '.';

export * as Messages from '../messages/role';

export enum Permission {
  MANAGE_USERS = 'manage_users',
  MANAGE_ROLES = 'manage_roles',
  MANAGE_USERS2 = 'manage_users2',
  MANAGE_ROLES2 = 'manage_roles2',
  MANAGE_USERS3 = 'manage_users3',
  MANAGE_ROLES3 = 'manage_roles3',
  MANAGE_USERS4 = 'manage_users4',
  MANAGE_ROLES4 = 'manage_roles4',
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
