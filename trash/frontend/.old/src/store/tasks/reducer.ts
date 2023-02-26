import { createSlice } from "@reduxjs/toolkit";

import { actions } from "./actions";
import { TasksState, FetchStatus } from "./types";

const initialTasksState: TasksState = {
  fetchStatus: FetchStatus.idle,
  tasks: [],
};

export const tasksSlice = createSlice({
  name: "tasks",
  initialState: initialTasksState,
  reducers: { ...actions },
});
