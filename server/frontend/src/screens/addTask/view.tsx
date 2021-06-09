import { FunctionComponent } from "react";
import { Card } from "primereact/card";

import { TaskUpload } from "components/taskUpload";

export type AddTaskViewProps = {
  file?: File;
  setFile: (file?: File) => void;
};

export const AddTaskView: FunctionComponent<AddTaskViewProps> = (props) => {
  if (props.file == null) return <TaskUpload file={props.file} setFile={props.setFile} />;
  return null;
};
