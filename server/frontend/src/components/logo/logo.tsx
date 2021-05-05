import { FunctionComponent } from "react";

import LogoImage from "./images/logo.png";

export const Logo: FunctionComponent<{
  className?: React.HTMLAttributes<HTMLImageElement>["className"];
  style?: React.HTMLAttributes<HTMLImageElement>["style"];
}> = (props) => {
  return <img className={props.className} style={props.style} draggable={false} src={LogoImage} alt="logo" />;
};
