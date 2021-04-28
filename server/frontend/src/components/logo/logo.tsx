import React, { FunctionComponent } from "react";
import "./logo.scss";
import LogoImage from "./images/logo53x53.png";

export const Logo: FunctionComponent = () => {
  return <img draggable={false} className="logo" src={LogoImage} alt="logo" />;
};
