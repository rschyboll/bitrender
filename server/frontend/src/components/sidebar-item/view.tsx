import { FunctionComponent } from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { Button } from "primereact/button";

import { SidebarItemProps } from ".";

export const SidebarItemView: FunctionComponent<SidebarItemProps> = (props) => {
  const { t } = useTranslation();

  const linkClassName = `sidebar-item ${props.highlighted ? "sidebar-item-highlighted" : null}`;
  const buttonClassName = `p-button-text p-button-plain`;

  return (
    <Link className={linkClassName} to={props.path}>
      <Button className={buttonClassName} label={t(props.label)} icon={props.icon} />
    </Link>
  );
};
