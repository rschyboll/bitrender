import { FunctionComponent, useState } from "react";

import { AddTaskView } from "./view";

export const AddTask: FunctionComponent = () => {
  const [file, setFile] = useState<File>();

  return <AddTaskView file={file} setFile={setFile} />;
};
