import { Button } from 'primereact/button';
import { Skeleton } from 'primereact/skeleton';
import { MouseEvent, memo } from 'react';
import { RiUserFill } from 'react-icons/ri';

import './style.scss';

export interface AvatarProps {
  onClick?: (e: MouseEvent) => void;
  name?: string;
}

export const Avatar = memo(function Avatar(props: AvatarProps) {
  if (props.name == null) {
    return <Skeleton width="8rem" height="2.5rem" />;
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
