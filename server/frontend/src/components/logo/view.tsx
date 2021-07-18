import { FunctionComponent } from "react";

import LogoImage from "./images/logo.png";
import { LogoProps } from ".";

export const LogoView: FunctionComponent<LogoProps> = (props) => {
  return <img className={props.className} style={props.style} draggable={false} src={LogoImage} alt="logo" />;
};
