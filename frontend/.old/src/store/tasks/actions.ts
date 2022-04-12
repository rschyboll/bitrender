import { PayloadAction } from "@reduxjs/toolkit";
import { FetchStatus, TasksState, TaskData } from "./types";

export const actions = {
  fetchStart: (state: TasksState) => {
    state.fetchStatus = FetchStatus.loading;
  },
  fetchSuccess: (state: TasksState, action: PayloadAction<TaskData[]>) => {
    state.fetchStatus = FetchStatus.success;
    state.tasks = action.payload;
  },
  fetchError: (state: TasksState) => {
    state.fetchStatus = FetchStatus.error;
  },
};
