import { useValues } from 'kea';
import { FC } from 'react';
import { useLocation } from 'react-router-dom';

import { Logo } from '@/components/logo';
import { settingsLogic } from '@/logic/settings';

import './style.scss';

export const SidebarHorizontal: FC = () => {
  const location = useLocation();
  const { sidebarType } = useValues(settingsLogic);

  return (
    <div className="sidebar-horizontal">
      <Logo />
      <ul className="sidebar-container"></ul>
    </div>
  );
};

const SidebarHorizontalGroup: FC = () => {};
