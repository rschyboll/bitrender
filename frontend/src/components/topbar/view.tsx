import { FunctionComponent } from "react";
import { useTranslation } from "react-i18next";

export type TopbarViewProps = { pathName: string };

export const TopbarView: FunctionComponent<TopbarViewProps> = (props) => {
  const { t } = useTranslation();

  return (
    <div id="topbar">
      <div id="topbar-left">
        <span id="topbar-viewname">{t(`navigation.${props.pathName}`)}</span>
      </div>
      <div id="topbar-right"></div>
    </div>
  );
};
