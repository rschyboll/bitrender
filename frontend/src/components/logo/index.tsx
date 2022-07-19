import { memo } from 'react';
import { Link } from 'react-router-dom';

import './style.scss';

const logo = new URL('../../assets/logo.svg', import.meta.url);

export interface LogoProps {
  titleVisible?: boolean;
}

export const Logo = memo(function Logo(props: LogoProps) {
  return (
    <Link className="logo" to="/">
      <img
        id="app-logo"
        className="logo-image"
        src={logo.toString()}
        alt="diamond layout"
      />
      {props.titleVisible && <span className="app-name">BITRENDER</span>}
    </Link>
  );
});
