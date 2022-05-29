import { useValues } from 'kea';
import { FC, memo } from 'react';

import { settingsLogic } from '@/logic/settings';
import { SidebarType } from '@/logic/settings/types';

import { SidebarHorizontal } from './horizontal';
import { SidebarSlim } from './slim';
import './style.scss';
import { SidebarWide } from './wide';

export interface SidebarProps {
  sidebarKey: string;
  types: SidebarType[];
}

export const Sidebar: FC<SidebarProps> = memo((props) => {
  const { sidebarType } = useValues(settingsLogic);

  return (
    <>
      <div
        className={
          sidebarType === SidebarType.Horizontal &&
          props.types.includes(sidebarType)
            ? 'w-full'
            : 'hidden'
        }
      >
        <SidebarHorizontal />
      </div>
      <div
        className={
          sidebarType === SidebarType.Slim && props.types.includes(sidebarType)
            ? 'h-full'
            : 'hidden'
        }
      >
        <SidebarSlim />
      </div>
      <div
        className={
          sidebarType === SidebarType.Static &&
          props.types.includes(sidebarType)
            ? 'h-full'
            : 'hidden'
        }
      >
        <SidebarWide />
      </div>
    </>
  );
});
