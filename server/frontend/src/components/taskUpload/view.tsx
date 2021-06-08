import { FunctionComponent, RefObject } from "react";
import { useTranslation } from "react-i18next";
import { DropzoneRootProps, DropzoneInputProps, FileWithPath, FileRejection } from "react-dropzone";

import { Card } from "primereact/card";
import { Messages } from "primereact/messages";

import BlenderLogo from "img/blender.svg";

export type TaskUploadViewProps = {
  acceptedFiles: FileWithPath[];
  rejectedFiles: FileRejection[];
  getRootProps: (props?: DropzoneRootProps) => DropzoneRootProps;
  getInputProps: (props?: DropzoneInputProps) => DropzoneInputProps;
  isOver: boolean;
  messagesRef: RefObject<Messages>;
};

const getSectionClassName = (isOver: boolean) => {
  return `fileDrop ${isOver ? "focus" : null}`;
};

export const TaskUploadView: FunctionComponent<TaskUploadViewProps> = (props) => {
  const { t } = useTranslation();

  const sectionClassName = getSectionClassName(props.isOver);
  const sectionProps = props.getRootProps({ className: sectionClassName });
  const inputProps = props.getInputProps();

  return (
    <>
      <Card className="fileDropCard">
        <section {...sectionProps}>
          <input {...inputProps} />
          <img src={BlenderLogo} alt="Blender logo" className="p-mt-3 p-p-5 fileDropImage" />
          <span className="fileDropText">{t("addTask.drop")}</span>
        </section>
      </Card>
      <Messages ref={props.messagesRef} />
    </>
  );
};
