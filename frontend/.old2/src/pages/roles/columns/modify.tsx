import { memo } from 'react';

import { RoleTableView } from '@/schemas/role';

export interface ModifyColumnProps {
  value: RoleTableView;
}

export const ModifyColumn = memo(function ModifyColumn(
  props: ModifyColumnProps,
) {
  return <div></div>;
});
