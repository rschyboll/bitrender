import { RoleColumns, RoleView } from '@/schemas/role';
import { ListRequestInput } from '@/services/messages/list';

export type GetRolesInput = ListRequestInput<RoleColumns>;

export type GetRolesOutput = RoleView[];
