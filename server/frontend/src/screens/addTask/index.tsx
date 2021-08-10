import { FunctionComponent, useState } from "react";

import axios from "axiosInstance";
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

  const uploadFile = async () => {
    if (file != null) {
      const data = new FormData();
      data.append("file", file);
      data.append("data", JSON.stringify({ name: "asd", rendering_engine: "", sample_amount: "1" }));

      try {
        const promise = await axios({ method: "post", url: "/tasks/new", data: data });
        console.log(promise);
        if (promise.status === 200) {
          console.log("ok");
        }
      } catch (error) {
        console.log(error);
      }
    }
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
      uploadFile={uploadFile}
    />
  );
};
