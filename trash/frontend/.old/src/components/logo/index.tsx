import { FunctionComponent } from "react";

import { LogoView } from "./view";

export type LogoProps = {
  className?: React.HTMLAttributes<HTMLImageElement>["className"];
  style?: React.HTMLAttributes<HTMLImageElement>["style"];
};

export const Logo: FunctionComponent<LogoProps> = (props) => {
  return <LogoView {...props} />;
};
