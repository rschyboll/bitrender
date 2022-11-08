import { MRole } from "@/types/models";

import { BaseView } from ".";

export interface UserView extends BaseView {
  email: string;
  username: string;
  role: string;
  permissions: MRole.Permission[];
}

export interface UserCreate {
  email: string;
  username: string;
  password: string;
}
