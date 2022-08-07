import { Button } from 'primereact/button';
import { Skeleton } from 'primereact/skeleton';
import { memo } from 'react';
import { RiUserFill } from 'react-icons/ri';

import './style.scss';

export interface AvatarProps {
  onClick?: () => void;
  name?: string;
}

export const Avatar = memo(function Avatar(props: AvatarProps) {
  if (props.name == null) {
    return <Skeleton />;
  }

  return (
    <Button
      className="avatar p-button-text p-button-secondary"
      onClick={props.onClick}
      label={props.name}
      icon={
        <div className="avatar-image">
          <RiUserFill className="avatar-icon" />
        </div>
      }
    />
  );
});
