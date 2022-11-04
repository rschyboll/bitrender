import { BaseColumns, BaseView } from '.';

export enum Permission {
  MANAGE_USERS = 'manage_users',
  MANAGE_ROLES = 'manage_roles',
}

export interface RoleView extends BaseView {
  name: string;
  default: true | null;
  permissions: Permission[];
}

export type RoleTableView = {
  name: string;
  default: true | null;
} & { [Key in Permission]: true | null };

export type RoleColumns = BaseColumns | 'name' | 'default';

export const RoleColumns: RoleColumns[] = [...BaseColumns, 'name', 'default'];
