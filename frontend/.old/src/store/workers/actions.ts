import { PayloadAction } from "@reduxjs/toolkit";
import { WorkersState, FetchStatus, WorkerData } from "./types";

export const actions = {
  fetchStart: (state: WorkersState) => {
    state.fetchStatus = FetchStatus.loading;
  },
  fetchSuccess: (state: WorkersState, action: PayloadAction<WorkerData[]>) => {
    state.fetchStatus = FetchStatus.success;
    state.workers = action.payload;
  },
  fetchError: (state: WorkersState) => {
    state.fetchStatus = FetchStatus.error;
  },
  activate: (state: WorkersState, action: PayloadAction<{ id: string }>) => {},
};
