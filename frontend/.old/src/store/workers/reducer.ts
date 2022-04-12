import { createSlice } from "@reduxjs/toolkit";

import { actions } from "./actions";
import { WorkersState, FetchStatus } from "./types";

const initialWorkersState: WorkersState = {
  fetchStatus: FetchStatus.idle,
  workers: [],
};

export const workersSlice = createSlice({
  name: "workers",
  initialState: initialWorkersState,
  reducers: { ...actions },
});
