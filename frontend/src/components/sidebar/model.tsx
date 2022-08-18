import { IconType } from 'react-icons';
import { RiGroupFill, RiServerFill, RiShieldUserFill } from 'react-icons/ri';

import { Permission } from '@/schemas/user';

export interface Group {
  icon: IconType;
  title: string;
  items: Item[];
  spacer: boolean;
}

export interface Item {
  icon: IconType;
  iconSize?: string;
  title: string;
  path: string;
  requiredPermissions?: Permission[];
}

export const sidebarModel: Group[] = [
  {
    icon: RiServerFill,
    title: 'nav.system',
    items: [
      {
        icon: RiGroupFill,
        title: 'nav.users',
        path: '/app/admin/users',
        requiredPermissions: [Permission.MANAGE_USERS],
      },
      {
        icon: RiShieldUserFill,
        iconSize: '1.5rem',
        title: 'nav.roles',
        path: '/app/admin/roles',
        requiredPermissions: [Permission.MANAGE_ROLES, 'tess' as Permission],
      },
    ],
    spacer: true,
  },
];

export const filterVisibleItems = (
  items: Item[],
  permissions?: Permission[],
) => {
  const visibleItems: Item[] = [];

  if (permissions == null) {
    return visibleItems;
  }

  for (const item of items) {
    let hasPermission = true;
    if (item.requiredPermissions != null) {
      for (const requiredPermission of item.requiredPermissions) {
        if (!permissions.includes(requiredPermission)) {
          hasPermission = false;
        }
      }
    }
    if (hasPermission) {
      visibleItems.push(item);
    }
  }

  return visibleItems;
};
