import type { MBase } from ".";

export * as Messages from "../messages/role";

export enum Permission {
  MANAGE_USERS = "manage_users",
  MANAGE_ROLES = "manage_roles",
}

export interface View extends MBase.View {
  name: string;
  default: true | null;
  permissions: Permission[];
}

export type TableView = {
  name: string;
  default: true | null;
} & { [Key in Permission]: true | null };

export type Columns = MBase.Columns | "name" | "default";
