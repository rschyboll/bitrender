import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Button } from 'primereact/button';
import { OverlayPanel, OverlayPanelEventType } from 'primereact/overlaypanel';
import { FC, useCallback, useRef, useState } from 'react';

import { Avatar } from '@/components/avatar';
import { Sidebar } from '@/components/sidebar';
import { IAppLogic, ISettingsLogic } from '@/logic/interfaces';
import { SidebarType } from '@/types/settings';

import { TopbarAvatarDialog } from './avatarDialog';
import './style.scss';
import { TopbarTitle } from './title';

export const Topbar: FC = () => {
  const settingsLogic = useInjection(ISettingsLogic.$);
  const appLogic = useInjection(IAppLogic.$);

  const { currentUser } = useValues(appLogic);

  const { toggleSidebar } = useActions(settingsLogic);

  const [topbarDialogsRef, setTopbarDialogsRef] =
    useState<HTMLDivElement | null>(null);
  const avatarDialogRef = useRef<OverlayPanel>(null);

  const toggleAvatarDialog = useCallback((e: OverlayPanelEventType) => {
    avatarDialogRef.current?.toggle(e);
  }, []);

  return (
    <div className="topbar">
      <div className="topbar-sidebar-background" />
      <div className="topbar-container">
        <div className="topbar-sidebar">
          <Sidebar
            sidebarKey="sidebar-horizontal"
            types={[SidebarType.Horizontal]}
          />
        </div>
        <div className="topbar-content">
          <div className="topbar-content-left">
            <Button
              onClick={() => toggleSidebar()}
              className="mobile-sidebar-button"
              icon="ri-menu-line"
            />
            <TopbarTitle />
          </div>
          <div className="topbar-content-right">
            <div className="topbar-spacer" />
            <Avatar onClick={toggleAvatarDialog} name={currentUser?.username} />
            <OverlayPanel appendTo={topbarDialogsRef} ref={avatarDialogRef}>
              <TopbarAvatarDialog />
            </OverlayPanel>
          </div>
        </div>
      </div>
      <div ref={(ref) => setTopbarDialogsRef(ref)} className="topbar-dialogs" />
    </div>
  );
};
