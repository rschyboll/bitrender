export enum ColumnType {
  NUMBER,
  STRING,
  BOOL,
  BINARY,
  ICON,
  TAG,
  DATE,
  DATERANGE,
}

export interface ColumnDefinition {
  title: string;
  type: ColumnType;
}

export interface DataTableModel {
  columns: Record<string, ColumnDefinition>;
}
