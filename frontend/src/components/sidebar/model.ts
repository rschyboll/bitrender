export interface Group {
  icon: string;
  title: string;
  items: Item[];
  spacer: boolean;
}

export interface Item {
  icon: string;
  title: string;
  path: string;
}

export const sidebarModel: Group[] = [
  {
    icon: 'pi-users',
    title: 'Favorites',
    items: [
      { icon: 'ri-home-4-line', title: 'Role', path: '/' },
      { icon: 'ri-mail-unread-line', title: 'Role2', path: '2' },
    ],
    spacer: true,
  },
  {
    icon: 'pi-users',
    title: 'nav.users',
    items: [
      { icon: 'ri-stack-line', title: 'Role', path: '1' },
      { icon: 'ri-chat-settings-line', title: 'Role2', path: '2' },
    ],
    spacer: true,
  },
  {
    icon: 'pi-users',
    title: 'nav.users1',
    items: [
      { icon: 'ri-stack-line', title: 'Role', path: '1' },
      { icon: 'ri-chat-settings-line', title: 'Role2', path: '2' },
    ],
    spacer: true,
  },
  {
    icon: 'pi-users',
    title: 'nav.users2',
    items: [
      { icon: 'ri-stack-line', title: 'Role', path: '1' },
      { icon: 'ri-chat-settings-line', title: 'Role2', path: '2' },
      { icon: 'ri-stack-line', title: 'Role', path: '3' },
      { icon: 'ri-chat-settings-line', title: 'Role2', path: '6' },
      { icon: 'ri-stack-line', title: 'Role', path: '4' },
      { icon: 'ri-chat-settings-line', title: 'Role2', path: '5' },
    ],
    spacer: true,
  },
  {
    icon: 'pi-users',
    title: 'nav.users3',
    items: [
      { icon: 'ri-stack-line', title: 'Role', path: '1' },
      { icon: 'ri-chat-settings-line', title: 'Role2', path: '2' },
      { icon: 'ri-stack-line', title: 'Role', path: '3' },
      { icon: 'ri-chat-settings-line', title: 'Role2', path: '6' },
      { icon: 'ri-stack-line', title: 'Role', path: '4' },
      { icon: 'ri-chat-settings-line', title: 'Role2', path: '5' },
    ],
    spacer: true,
  },
  {
    icon: 'pi-users',
    title: 'nav.users4',
    items: [
      { icon: '', title: 'Role', path: '1' },
      { icon: '', title: 'Role2', path: '2' },
    ],
    spacer: true,
  },
  {
    icon: 'pi-users',
    title: 'nav.users5',
    items: [
      { icon: '', title: 'Role', path: '1' },
      { icon: '', title: 'Role2', path: '2' },
    ],
    spacer: false,
  },
];
