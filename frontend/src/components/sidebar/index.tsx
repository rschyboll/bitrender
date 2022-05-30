import { useValues } from 'kea';
import { FC, memo } from 'react';

import Dependencies from '@/deps';
import { ISettingsLogic } from '@/logic/interfaces';
import { SidebarType } from '@/logic/settings/types';

import { SidebarHorizontal } from './horizontal';
import { SidebarMobile } from './mobile';
import { SidebarSlim } from './slim';
import './style.scss';
import { SidebarWide } from './wide';

export interface SidebarProps {
  sidebarKey: string;
  types: SidebarType[];
}

export const Sidebar: FC<SidebarProps> = memo((props) => {
  const settingsLogic: ISettingsLogic = Dependencies.use('LOGIC', 'SETTINGS');
  const { sidebarType } = useValues(settingsLogic);

  return (
    <>
      <SidebarMobile />
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
