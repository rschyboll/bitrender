import { FormEvent, FunctionComponent, useState } from "react";

import { AddTaskView } from "./view";
import "./style.scss";

export const AddTask: FunctionComponent = () => {
  const [file, setFile] = useState<File>();
  const [renderingEngine, setRenderingEngine] = useState<string>("cycles");
  const [sampleAmount, setSampleAmount] = useState<number>(100);

  const changeRenderingEngine = (event: { value: string }) => {
    setRenderingEngine(event.value);
  };

  const changeSampleAmount = (event: React.FormEvent<HTMLInputElement>) => {
    setSampleAmount(parseInt(event.currentTarget.value));
  };

  const abortTask = () => {
    setFile(undefined);
    setRenderingEngine("cycles");
    setSampleAmount(100);
  };

  return (
    <AddTaskView
      renderingEngine={renderingEngine}
      setRenderingEngine={changeRenderingEngine}
      file={file}
      setFile={setFile}
      sampleAmount={sampleAmount}
      setSampleAmount={changeSampleAmount}
      abortTask={abortTask}
    />
  );
};
