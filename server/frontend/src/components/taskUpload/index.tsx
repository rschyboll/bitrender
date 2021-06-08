import { FunctionComponent, useRef } from "react";
import { useDropzone, FileRejection } from "react-dropzone";
import { Messages } from "primereact/messages";
import { useTranslation } from "react-i18next";

import { TaskUploadView } from "./view";
import "./style.scss";

export type TaskUploadProps = {};

export const TaskUpload: FunctionComponent<TaskUploadProps> = (props) => {
  const { t } = useTranslation();
  const onDropRejected = (files: FileRejection[]) => {
    const summary = t("addTask.wrongFile", { file: files[files.length - 1].file.name });
    messagesRef.current?.show({ life: 5000, severity: "error", summary });
  };

  const { acceptedFiles, getRootProps, getInputProps, isDragActive, fileRejections } = useDropzone({
    maxFiles: 1,
    accept: ".blend",
    onDropRejected,
  });

  const messagesRef = useRef<Messages>(null);

  return (
    <TaskUploadView
      acceptedFiles={acceptedFiles}
      rejectedFiles={fileRejections}
      getRootProps={getRootProps}
      getInputProps={getInputProps}
      isOver={isDragActive}
      messagesRef={messagesRef}
    />
  );
};
