import { FunctionComponent } from "react";
import { Card } from "primereact/card";

import { TaskUpload } from "components/taskUpload";

export const AddTaskView: FunctionComponent = () => {
  return (
    <Card>
      <TaskUpload />
    </Card>
  );
};
