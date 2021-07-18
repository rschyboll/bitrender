import { FormEvent, FunctionComponent } from "react";
import { Card } from "primereact/card";
import { Button } from "primereact/button";
import { Dropdown, DropdownChangeParams } from "primereact/dropdown";
import { InputText } from "primereact/inputtext";
import { useTranslation } from "react-i18next";

import { TaskUpload } from "components/taskUpload";
import { getFileSizeInMB } from "./logic";

const renderingEngines = [
  { label: "addTask.config.cycles", value: "cycles" },
  { label: "addTask.config.eevee", value: "eevee" },
];

export type AddTaskViewProps = {
  file?: File;
  setFile: (file?: File) => void;
  renderingEngine: string;
  setRenderingEngine: (event: DropdownChangeParams) => void;
  sampleAmount: number;
  setSampleAmount: (event: React.FormEvent<HTMLInputElement>) => void;
  abortTask: () => void;
};

export const AddTaskView: FunctionComponent<AddTaskViewProps> = (props) => {
  const { t } = useTranslation();

  if (props.file == null) {
    return <TaskUpload file={props.file} setFile={props.setFile} />;
  }
  return (
    <Card>
      <Button
        onClick={props.abortTask}
        className="p-button-rounded p-button-secondary p-button-outlined abortButton"
        icon="pi pi-times"
      />
      <div className="p-fluid" style={{ width: "35%" }}>
        <h5>{t("addTask.config.projectSettings")}</h5>
        <p>
          {t("addTask.config.projectSize")}: {getFileSizeInMB(props.file.size)}
        </p>
        <p>
          {t("addTask.config.projectName")}: {props.file.name}
        </p>
        <h5>{t("addTask.config.renderSettings")}</h5>
        <div className="p-field">
          <label htmlFor="fieldId">{t("addTask.config.renderEngine")}</label>
          <Dropdown
            options={renderingEngines}
            value={props.renderingEngine}
            onChange={props.setRenderingEngine}
            itemTemplate={(option: { label: string; code: string }) => t(option.label)}
            valueTemplate={(option: { label: string; code: string }) => t(option.label)}
          />
        </div>
        <div className="p-field">
          <label htmlFor="fieldId">{t("addTask.config.sampleAmount")}</label>
          <InputText type="number" value={props.sampleAmount} onChange={props.setSampleAmount} />
        </div>
      </div>
      <Button label={t("addTask.config.upload")} />
    </Card>
  );
};
