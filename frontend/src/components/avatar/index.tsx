import { memo } from 'react';

export interface AvatarProps {
  onClick?: () => void;
  image?: string;
  name?: string;
}

export const Avatar = memo(function Avatar(props: AvatarProps) {
  return (
    <button className="avatar" onClick={props.onClick}>
      {props.image != null ? <img className="avatar-image" /> : null}
    </button>
  );
});
