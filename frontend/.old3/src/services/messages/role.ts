import { RoleColumns, RoleView } from '@/schemas/role';
import { ListRequestInput, ListRequestOutput } from '@/services/messages/list';

export type GetRolesInput = ListRequestInput<RoleColumns>;

export type GetRolesOutput = ListRequestOutput<RoleView[]>;
