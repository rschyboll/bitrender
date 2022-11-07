import { BaseColumns, BaseView } from ".";

interface RoleView extends BaseView {
  name: string;
  default: true | null;
  permissions: Permission[];
}

type RoleTableView = {
  name: string;
  default: true | null;
} & { [Key in Permission]: true | null };

type RoleColumns = BaseColumns | "name" | "default";

const RoleColumns: RoleColumns[] = [...BaseColumns, "name", "default"];
