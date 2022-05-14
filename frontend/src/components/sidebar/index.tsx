import { PanelMenu } from 'primereact/panelmenu';
import { FC, useState } from 'react';
import { useLocation } from 'react-router-dom';

import { SidebarGroup } from '../sidebar-group';
import { SidebarItem } from '../sidebar-item';
import './style.scss';

const groups = {
  user: {
    icon: '',
    title: '',
    items: [
      { icon: '', title: 'TEST', path: '' },
      { icon: '', title: '', path: '' },
    ],
  },
  tasks: {
    icon: '',
    title: '',
    items: [
      { icon: '', title: '', path: '' },
      { icon: '', title: '', path: '' },
    ],
  },
};

export const Sidebar: FC = () => {
  const [openItem, setOpenItem] = useState<String | null>(null);
  const location = useLocation();

  return (
    <div className="sidebar flex flex-column">
      {Object.entries(groups).map((groupEntry) => {
        return (
          <SidebarGroup
            key={groupEntry[0]}
            open={groupEntry[0] == openItem}
            onOpen={setOpenItem}
            {...groupEntry[1]}
          >
            {groupEntry[1].items.map((item) => {
              return (
                <SidebarItem
                  current={location.pathname == item.path}
                  {...item}
                />
              );
            })}
          </SidebarGroup>
        );
      })}
    </div>
  );
};
