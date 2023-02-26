import { ColumnType, DataTableModel } from '@/components/dataTable';
import { Permission, RoleTableView } from '@/schemas/role';

const createPermissionModelColumns = () => {
  return Object.fromEntries(
    Object.values(Permission).map((permission) => [
      permission,
      {
        title: `permission.${permission}`,
        type: ColumnType.TRUEORNULL,
      },
    ]),
  ) as {
    [Key in Permission]: {
      title: string;
      type: ColumnType.TRUEORNULL;
    };
  };
};

export const rolesTableModel: DataTableModel<RoleTableView> = {
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
