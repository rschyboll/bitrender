import { useValues } from 'kea';
import { FC } from 'react';
import { useLocation } from 'react-router-dom';

import { Logo } from '@/components/logo';
import { settingsLogic } from '@/logic/settings';

import './style.scss';

export const SidebarSlim: FC = () => {
  const location = useLocation();
  const { sidebarType } = useValues(settingsLogic);

  return (
    <div className="sidebar-slim">
      <Logo />
    </div>
  );
};

const SidebarGroupSlim = () => {};

const SidebarItemSlim = () => {};
