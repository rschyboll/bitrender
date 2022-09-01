import { Ripple } from 'primereact/ripple';
import { memo } from 'react';
import { Trans } from 'react-i18next';
import { IconType } from 'react-icons';
import { Link } from 'react-router-dom';

import './style.scss';

export interface TopbarDialogItemProps {
  icon: IconType;
  iconSize?: string;
  title: string;
  path?: string;
  onClick?: () => void;
}

export const TopbarDialogItem = memo(function TopbarDialogItem({
  icon,
  iconSize,
  title,
  path,
  onClick,
}: TopbarDialogItemProps) {
  if (path != null) {
    return (
      <Link className="topbar-dialog-item p-ripple" to={path}>
        <TopbarDialogItemBody icon={icon} iconSize={iconSize} title={title} />
      </Link>
    );
  }
  return (
    <div className="topbar-dialog-item p-ripple" onClick={onClick}>
      <TopbarDialogItemBody icon={icon} iconSize={iconSize} title={title} />
    </div>
  );
});

interface TopbarDialogItemBodyProps {
  icon: IconType;
  iconSize?: string;
  title: string;
}

const TopbarDialogItemBody = ({
  iconSize,
  title,
  ...props
}: TopbarDialogItemBodyProps) => {
  return (
    <>
      <div className="topbar-dialog-item-icon-container">
        <props.icon
          style={{
            top:
              iconSize != null ? `calc((1.2rem - ${iconSize})/2)` : undefined,
            left:
              iconSize != null ? `calc((1.2rem - ${iconSize})/2)` : undefined,
          }}
          size={iconSize != null ? iconSize : '1.2rem'}
          className="topbar-dialog-item-icon"
        />
      </div>
      <span className="topbar-dialog-item-title">
        <Trans>{title}</Trans>
      </span>
      <Ripple />
    </>
  );
};
