import { useSelector } from "react-redux";

import { StoreState } from "store";
import { TaskData, FetchStatus } from "./types";

export const tasksSelectors = {
  useTasksData: () => {
    return useSelector<StoreState, TaskData[]>((state) => {
      return state.tasks.tasks;
    });
  },
  useTasksFetchStatus: () => {
    return useSelector<StoreState, FetchStatus>((state) => {
      return state.tasks.fetchStatus;
    });
  },
};
