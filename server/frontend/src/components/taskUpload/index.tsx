import { FunctionComponent, useRef } from "react";
import { useTranslation } from "react-i18next";
import { FileRejection } from "react-dropzone";
import { Messages } from "primereact/messages";

import { TaskUploadView } from "./view";
import "./style.scss";

export type TaskUploadProps = {
  file?: File;
  setFile: (file?: File) => void;
};

export const TaskUpload: FunctionComponent<TaskUploadProps> = (props) => {
  const { t } = useTranslation();
  const messagesRef = useRef<Messages>(null);

  const onDropRejected = (files: FileRejection[]) => {
    const fileName = files[files.length - 1].file.name;
    const summary = t("addTask.wrongFile", { file: fileName });
    messagesRef.current?.show({ life: 5000, severity: "error", summary });
  };

  const onDropAccepted = (files: File[]) => {
    props.setFile(files[0]);
  };

  return <TaskUploadView messagesRef={messagesRef} onDropAccepted={onDropAccepted} onDropRejected={onDropRejected} />;
};
