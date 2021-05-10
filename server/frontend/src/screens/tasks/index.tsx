import { FunctionComponent } from "react";

import { TasksView } from "./view";
import "./style.scss";

export type TasksProps = {};

export const Tasks: FunctionComponent<TasksProps> = () => {
  return <TasksView />;
};
