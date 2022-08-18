import { memo } from 'react';
import { Trans } from 'react-i18next';
import { IconType } from 'react-icons';
import { Link } from 'react-router-dom';

export interface TopbarDialogItemProps {
  icon: IconType;
  iconSize?: string;
  title: string;
  path?: string;
  onClick: () => void;
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
      <Link to={path}>
        <TopbarDialogItemBody icon={icon} iconSize={iconSize} title={title} />
      </Link>
    );
  }
  return (
    <div onClick={onClick}>
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
      <div className="topbar-item-icon-container">
        <props.icon
          style={{
            top:
              iconSize != null ? `calc((1.2rem - ${iconSize})/2)` : undefined,
            left:
              iconSize != null ? `calc((1.2rem - ${iconSize})/2)` : undefined,
          }}
          size={iconSize != null ? iconSize : '1.2rem'}
          className="topbar-item-icon"
        />
      </div>
      <span className="topbar-item-title">
        <Trans>{title}</Trans>
      </span>
    </>
  );
};
