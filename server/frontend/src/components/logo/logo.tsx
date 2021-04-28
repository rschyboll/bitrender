import { FunctionComponent } from "react";

import LogoImage from "./images/logo.png";

export const Logo: FunctionComponent<{ className: string }> = (props) => {
  return <img {...props} draggable={false} src={LogoImage} alt="logo" />;
};
