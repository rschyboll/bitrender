import { ColumnType, DataTableModel } from '@/components/dataTable/model';

export const rolesTableModel: DataTableModel = {
  columns: {
    name: {
      title: 'role.name',
      type: ColumnType.STRING,
    },
  },
};
