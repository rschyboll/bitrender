import { IconType } from 'react-icons';
import {
  RiAppleFill,
  RiGroupFill,
  RiServerFill,
  RiShieldUserFill,
} from 'react-icons/ri';

import { Permission } from '@/types/user';

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
    icon: RiAppleFill,
    title: 'Favorites',
    items: [
      { icon: RiAppleFill, title: 'Role', path: '/' },
      { icon: RiAppleFill, title: 'Role2', path: '2' },
    ],
    spacer: true,
  },
  {
    icon: RiGroupFill,
    title: 'nav.users',
    items: [
      { icon: RiGroupFill, title: 'nav.users', path: '1' },
      { icon: RiAppleFill, title: 'Role2', path: '2' },
    ],
    spacer: true,
  },
  {
    icon: RiServerFill,
    title: 'nav.system',
    items: [
      { icon: RiGroupFill, title: 'nav.users', path: '/app/admin/users' },
      {
        icon: RiShieldUserFill,
        iconSize: '1.5rem',
        title: 'nav.roles',
        path: '/app/admin/roles',
      },
    ],
    spacer: true,
  },
];
