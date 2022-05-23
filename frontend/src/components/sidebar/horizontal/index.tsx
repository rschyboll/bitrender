import { useValues } from 'kea';
import { FC, memo, useMemo, useState } from 'react';
import { useLocation } from 'react-router-dom';

import { Logo } from '@/components/logo';
import { settingsLogic } from '@/logic/settings';

import { Group, sidebarModel } from '../model';
import './style.scss';

export const SidebarHorizontal: FC = memo(() => {
  const [activeGroup, setActiveGroup] = useState<string | null>(null);
  const location = useLocation();

  const currentGroup = useMemo(() => {
    return Object.values(sidebarModel).find((group) => {
      return (
        group.items.find((item) => item.path == location.pathname) != undefined
      );
    });
  }, [location]);

  return (
    <div className="sidebar-horizontal">
      <Logo />
      <ul className="sidebar-container">
        {sidebarModel.map((groupModel) => {
          return (
            <SidebarHorizontalGroup
              key={groupModel.title}
              groupKey={groupModel.title}
              onMouseOver={setActiveGroup}
              active={activeGroup == groupModel.title}
              groupItemActive={currentGroup == groupModel}
              {...groupModel}
            />
          );
        })}
      </ul>
    </div>
  );
});

interface SidebarHorizontalGroupProps extends Group {
  groupKey: string;
  onMouseOver: (key: string) => void;
  active: boolean;
  groupItemActive: boolean;
}

const SidebarHorizontalGroup: FC<SidebarHorizontalGroupProps> = memo(
  (props) => {
    return <div></div>;
  },
);
