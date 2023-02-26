import { Permission } from '@/schemas/role';

import { BaseView } from '.';

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
