export interface View {
  id: string;
  createdAt: string;
  modifiedAt: string;
}

export type Columns = keyof View;
