import React, { FunctionComponent } from "react";
import { Card } from "primereact/card";
import { Button } from "primereact/button";
import { InputText } from "primereact/inputtext";
import { useTranslation } from "react-i18next";

import { TaskUpload } from "components/taskUpload";
import { getFileSizeInMB } from "./logic";

export type AddTaskViewProps = {
  file?: File;
  setFile: (file?: File) => void;
  sampleAmount: number;
  setSampleAmount: (event: React.FormEvent<HTMLInputElement>) => void;
  abortTask: () => void;
  uploadFile: () => void;
  changeXResolution: (event: React.FormEvent<HTMLInputElement>) => void;
  changeYResolution: (event: React.FormEvent<HTMLInputElement>) => void;
  xResolution: number;
  yResolution: number;
  changeStartFrame: (event: React.FormEvent<HTMLInputElement>) => void;
  changeEndFrame: (event: React.FormEvent<HTMLInputElement>) => void;
  startFrame: number;
  endFrame: number;
  uploading: boolean;
};

export const AddTaskView: FunctionComponent<AddTaskViewProps> = (props) => {
  const { t } = useTranslation();

  if (props.file == null) {
    return <TaskUpload file={props.file} setFile={props.setFile} />;
  }

  if (props.uploading) {
    return <Card>Wysyłanie w trakcie.</Card>;
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
          <label htmlFor="fieldId">{t("addTask.config.sampleAmount")}</label>
          <InputText
            type="number"
            value={props.sampleAmount}
            onChange={props.setSampleAmount}
          />
        </div>
        <div className="p-field">
          <label>{t("addTask.config.resolution")}</label>
          <div className="p-inputgroup">
            <span className="p-inputgroup-addon">
              <p>x</p>
            </span>
            <InputText
              type="number"
              value={props.xResolution}
              onChange={props.changeXResolution}
            />
            <span className="p-inputgroup-addon">
              <p>y</p>
            </span>
            <InputText
              type="number"
              value={props.yResolution}
              onChange={props.changeYResolution}
            />
          </div>
        </div>
        <div className="p-field">
          <label>{t("addTask.config.frames")}</label>
          <div className="p-inputgroup">
            <span className="p-inputgroup-addon">
              <p>Start</p>
            </span>
            <InputText
              type="number"
              value={props.startFrame}
              onChange={props.changeStartFrame}
            />
            <span className="p-inputgroup-addon">
              <p>End</p>
            </span>
            <InputText
              type="number"
              value={props.endFrame}
              onChange={props.changeEndFrame}
            />
          </div>
        </div>
      </div>
      <Button label={t("addTask.config.upload")} onClick={props.uploadFile} />
    </Card>
  );
};
