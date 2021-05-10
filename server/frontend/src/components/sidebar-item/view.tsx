import { FunctionComponent } from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { Button } from "primereact/button";

import { SidebarItemProps } from ".";

export const SidebarItemView: FunctionComponent<SidebarItemProps> = (props) => {
  const { t } = useTranslation();

  return (
    <Link className={`sidebar-item ${props.highlighted ? "sidebar-item-highlighted" : null}`} to={props.path}>
      <Button className="p-button-text p-button-plain" label={t(props.label)} icon={props.icon} />
    </Link>
  );
};
