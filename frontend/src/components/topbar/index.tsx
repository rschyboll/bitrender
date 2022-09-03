import { useInjection } from 'inversify-react';
import { useActions, useValues } from 'kea';
import { Button } from 'primereact/button';
import { OverlayPanel, OverlayPanelEventType } from 'primereact/overlaypanel';
import { FC, useCallback, useRef } from 'react';

import { Avatar } from '@/components/avatar';
import { Sidebar } from '@/components/sidebar';
import { IAppLogic, ISettingsLogic } from '@/logic/interfaces';
import { SidebarType, Theme } from '@/types/settings';

import { TopbarAvatarDialog } from './avatarDialog';
import './style.scss';

export const Topbar: FC = () => {
  const settingsLogic = useInjection(ISettingsLogic.$);
  const appLogic = useInjection(IAppLogic.$);

  const { currentUser } = useValues(appLogic);

  const { toggleSidebar, setSidebarType, setTheme } = useActions(settingsLogic);

  const topbarDialogsRef = useRef<HTMLDivElement>(null);
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
          </div>
          <div className="topbar-content-right">
            <div className="topbar-spacer" />
            <Avatar onClick={toggleAvatarDialog} name={currentUser?.username} />
            <Button
              label="Horizontal"
              onClick={() => setSidebarType(SidebarType.Horizontal)}
            />
            <Button
              label="Slim"
              onClick={() => setSidebarType(SidebarType.Slim)}
            />
            <Button
              label="Static"
              onClick={() => setSidebarType(SidebarType.Static)}
            />
            <Button label="Dark" onClick={() => setTheme(Theme.Dark)} />
            <Button label="Dim" onClick={() => setTheme(Theme.Dim)} />
            <Button label="Light" onClick={() => setTheme(Theme.Light)} />

            <OverlayPanel
              appendTo={topbarDialogsRef.current}
              ref={avatarDialogRef}
            >
              <TopbarAvatarDialog />
            </OverlayPanel>
          </div>
        </div>
      </div>
      <div ref={topbarDialogsRef} className="topbar-dialogs" />
    </div>
  );
};
