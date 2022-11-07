import { MRole } from "@/types/models";
import { ListRequestInput, ListRequestOutput } from "@/services/messages/list";

export type GetRolesInput = ListRequestInput<MRole.Columns>;

export type GetRolesOutput = ListRequestOutput<MRole.View[]>;
