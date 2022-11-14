import { ListRequestInput, ListRequestOutput } from '@/services/messages/list';
import { MRole } from '@/types/models';

export type GetListInput = ListRequestInput<MRole.Columns>;

export type GetListOutput = ListRequestOutput<MRole.View[]>;

export type CreateInput = MRole.Create;

export type CreateOutput = MRole.View;
