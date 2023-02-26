import { memo } from 'react';

import './style.scss';

export interface SidebarDialogProps {
  active: boolean;
  children: JSX.Element[];
}

export const SidebarDialog = memo(function SidebarDialog(
  props: SidebarDialogProps,
) {
  return (
    <div className={props.active ? '' : 'hidden'}>
      <div
        className={`sidebar-dialog ${props.active && 'sidebar-dialog-active'}`}
      >
        <div className="sidebar-dialog-items">{props.children}</div>
      </div>
    </div>
  );
});
