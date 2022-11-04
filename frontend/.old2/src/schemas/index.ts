export interface BaseView {
  id: string;
  createdAt: string;
  modifiedAt: string;
}

export type BaseColumns = 'id' | 'created_at' | 'modified_at';

export const BaseColumns: BaseColumns[] = ['id', 'created_at', 'modified_at'];
