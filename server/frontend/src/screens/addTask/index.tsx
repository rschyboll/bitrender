import { FunctionComponent, useState } from "react";
import { useHistory } from "react-router-dom";

import axios from "axiosInstance";
import { AddTaskView } from "./view";
import "./style.scss";

export const AddTask: FunctionComponent = () => {
  const [uploading, setUploading] = useState(false);
  const [file, setFile] = useState<File>();
  const [resolution, setResolution] = useState({ x: 1920, y: 1080 });
  const [frames, setFrames] = useState({ start: 1, end: 100 });
  const [sampleAmount, setSampleAmount] = useState<number>(100);
  const history = useHistory();

  const changeXResolution = (event: React.FormEvent<HTMLInputElement>) => {
    let value = event.currentTarget.value;
    let intValue = parseInt(value);
    if (!isNaN(intValue)) {
      setResolution({ ...resolution, x: intValue });
    }
  };

  const changeYResolution = (event: React.FormEvent<HTMLInputElement>) => {
    let value = event.currentTarget.value;
    let intValue = parseInt(value);
    if (!isNaN(intValue)) {
      setResolution({ ...resolution, y: intValue });
    }
  };

  const changeStartFrame = (event: React.FormEvent<HTMLInputElement>) => {
    let value = event.currentTarget.value;
    let intValue = parseInt(value);
    if (!isNaN(intValue)) {
      setFrames({ ...frames, start: intValue });
    }
  };

  const changeEndFrame = (event: React.FormEvent<HTMLInputElement>) => {
    let value = event.currentTarget.value;
    let intValue = parseInt(value);
    if (!isNaN(intValue)) {
      setFrames({ ...frames, end: intValue });
    }
  };

  const changeSampleAmount = (event: React.FormEvent<HTMLInputElement>) => {
    setSampleAmount(parseInt(event.currentTarget.value));
  };

  const abortTask = () => {
    setFile(undefined);
    setResolution({ x: 1920, y: 1080 });
    setFrames({ start: 1, end: 100 });
    setSampleAmount(100);
    setUploading(false);
    history.push("/tasks");
  };

  const uploadFile = async () => {
    if (file != null) {
      const data = new FormData();
      data.append("file", file);
      data.append("samples", JSON.stringify(sampleAmount));
      data.append("start_frame", JSON.stringify(frames.start));
      data.append("end_frame", JSON.stringify(frames.end));
      data.append("resolution_x", JSON.stringify(resolution.x));
      data.append("resolution_y", JSON.stringify(resolution.y));

      setUploading(true);
      try {
        const promise = await axios({
          method: "post",
          url: "/tasks/new",
          data: data,
        });
        console.log(promise);
        if (promise.status === 201) {
          console.log("ok");
        }
      } catch (error) {
        console.log(error);
      }
      abortTask();
    }
  };

  return (
    <AddTaskView
      file={file}
      setFile={setFile}
      sampleAmount={sampleAmount}
      setSampleAmount={changeSampleAmount}
      abortTask={abortTask}
      uploadFile={uploadFile}
      changeXResolution={changeXResolution}
      changeYResolution={changeYResolution}
      xResolution={resolution.x}
      yResolution={resolution.y}
      changeStartFrame={changeStartFrame}
      changeEndFrame={changeEndFrame}
      startFrame={frames.start}
      endFrame={frames.end}
      uploading={uploading}
    />
  );
};
