import React, { FunctionComponent, useState } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "primereact/button";
import { Dialog } from "primereact/dialog";
import { InputText } from "primereact/inputtext";

export type BinariesDialogProps = {
  dialogVisible: boolean;
  showDialog: (arg0: boolean) => void;
  addNewBinary: (url: string, version: string) => void;
};

export const BinariesDialog: FunctionComponent<BinariesDialogProps> = (
  props
) => {
  const { t } = useTranslation();

  const [url, setUrl] = useState("");
  const [version, setVersion] = useState("");

  const header = t("binaries.provide_data");
  const onAccept = () => {
    if (url !== "" && version !== "") {
      props.addNewBinary(url, version);
      setUrl("");
      setVersion("");
    }
  };
  const footer = () => (
    <Button onClick={onAccept} label={t("binaries.accept")} />
  );
  const onHide = () => props.showDialog(false);

  const onUrlChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setUrl(event.target.value);
  };
  const onVersionChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setVersion(event.target.value);
  };

  return (
    <Dialog
      header={header}
      footer={footer}
      onHide={onHide}
      visible={props.dialogVisible}
    >
      <h5>{t("binaries.url")}</h5>
      <InputText
        value={url}
        onChange={onUrlChange}
        className="binaries-inputfield"
      />

      <h5> {t("binaries.version")}</h5>
      <InputText
        value={version}
        onChange={onVersionChange}
        className="binaries-inputfield"
      />
    </Dialog>
  );
};
