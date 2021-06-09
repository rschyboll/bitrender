import { FunctionComponent, RefObject } from "react";
import { useTranslation } from "react-i18next";
import Dropzone, { FileRejection } from "react-dropzone";
import { Card } from "primereact/card";
import { Messages } from "primereact/messages";

import BlenderLogo from "img/blender.svg";

export type TaskUploadViewProps = {
  messagesRef: RefObject<Messages>;
  onDropAccepted: (files: File[]) => void;
  onDropRejected: (files: FileRejection[]) => void;
};

const getSectionClassName = (isOver: boolean) => {
  return `fileDrop ${isOver ? "focus" : ""}`;
};

export const TaskUploadView: FunctionComponent<TaskUploadViewProps> = (props) => {
  const { t } = useTranslation();

  return (
    <>
      <Card className="fileDropCard">
        <Dropzone
          maxFiles={1}
          multiple={false}
          accept=".blend"
          onDropAccepted={props.onDropAccepted}
          onDropRejected={props.onDropRejected}
        >
          {({ getRootProps, getInputProps, isDragActive }) => {
            return (
              <section {...getRootProps({ className: getSectionClassName(isDragActive) })}>
                <input {...getInputProps()} />
                <img src={BlenderLogo} alt="Blender logo" className="p-mt-3 p-p-5 fileDropImage" />
                <span className="fileDropText">{t("addTask.drop")}</span>
              </section>
            );
          }}
        </Dropzone>
      </Card>
      <Messages ref={props.messagesRef} />
    </>
  );
};
