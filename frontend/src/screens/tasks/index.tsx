import { FunctionComponent, useEffect } from "react";
import { useDispatch } from "react-redux";

import { tasksSelectors } from "store/tasks/selectors";
import { tasksSlice } from "store/tasks/reducer";
import { TaskData } from "store/tasks/types";

import { TasksView } from "./view";
import axios from "axiosInstance";
import "./style.scss";

export type TasksProps = {};

export const Tasks: FunctionComponent<TasksProps> = () => {
  const dispatch = useDispatch();
  const tasks = tasksSelectors.useTasksData();

  useEffect(() => {
    dispatch(tasksSlice.actions.fetchStart());
  }, [dispatch]);

  const deleteTask = async (task: TaskData) => {
    try {
      await axios({
        method: "delete",
        url: `/tasks/${task.id}`,
      });
    } catch (e) {}

    dispatch(tasksSlice.actions.fetchStart());
  };

  return <TasksView tasks={tasks} deleteTask={deleteTask} />;
};
