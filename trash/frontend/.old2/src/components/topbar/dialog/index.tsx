import { memo } from 'react';

import './style.scss';

export interface TopbarDialog {
  children: JSX.Element[] | JSX.Element;
}

export const TopbarDialog = memo(function TopbarDialog(props: TopbarDialog) {
  return <div className="topbar-dialog">{props.children}</div>;
});
