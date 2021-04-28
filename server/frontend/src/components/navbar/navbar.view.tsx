import React, { FunctionComponent } from "react";
import "./navbar.scss";
import { Menubar } from "primereact/menubar";
import { Logo } from "../logo/logo";

export const NavbarView: FunctionComponent = () => {
  return <Menubar id="topbar" start={<Logo />} />;
};
