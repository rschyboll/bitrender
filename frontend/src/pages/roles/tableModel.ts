import { ColumnType, DataTableModel } from '@/components/dataTable';
import { MRole } from '@/types/models';

const createPermissionModelColumns = () => {
  return Object.fromEntries(
    Object.values(MRole.Permission).map((permission) => [
      permission,
      {
        title: `permission.${permission}`,
        type: ColumnType.BOOL,
      },
    ]),
  ) as {
    [Key in MRole.Permission]: {
      title: string;
      type: ColumnType.BOOL;
    };
  };
};

export const rolesTableModel: DataTableModel<MRole.TableView, 'id'> = {
  columns: {
    name: {
      title: 'role.name',
      type: ColumnType.STRING,
    },
    default: {
      title: 'role.default',
      type: ColumnType.TRUEORNULL,
    },
    ...createPermissionModelColumns(),
  },
};
