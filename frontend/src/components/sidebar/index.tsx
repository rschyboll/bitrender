import { useValues } from 'kea';
import { Ripple } from 'primereact/ripple';
import { FC, memo, useEffect, useState } from 'react';
import { CSSTransition, SwitchTransition } from 'react-transition-group';

import { settingsLogic } from '@/logic/settings';
import { SidebarType } from '@/logic/settings/types';

import { SidebarHorizontal } from './horizontal';
import { sidebarModel } from './model';
import { SidebarSlim } from './slim';
import './style.scss';
import { SidebarWide } from './wide';

const logo = new URL('../../assets/logo.svg', import.meta.url);

export interface SidebarProps {
  sidebarKey: string;
  types: SidebarType[];
}

export const Sidebar: FC<SidebarProps> = memo((props) => {
  const { sidebarType } = useValues(settingsLogic);

  return (
    <SwitchTransition key={props.sidebarKey}>
      <CSSTransition
        addEndListener={() => {}}
        classNames="sidebar-fade"
        key={props.sidebarKey + sidebarType.toString()}
        timeout={125}
        unmountOnExit
        mountOnEnter
      >
        <>
          {sidebarType == SidebarType.Horizontal &&
          sidebarType in props.types ? (
            <SidebarHorizontal />
          ) : null}
          {sidebarType == SidebarType.Slim &&
          props.types.includes(sidebarType) ? (
            <SidebarSlim />
          ) : null}
          {sidebarType == SidebarType.Static &&
          props.types.includes(sidebarType) ? (
            <SidebarWide />
          ) : null}
        </>
      </CSSTransition>
    </SwitchTransition>
  );
});
