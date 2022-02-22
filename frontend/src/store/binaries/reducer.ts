import { createSlice } from "@reduxjs/toolkit";

import { actions } from "./actions";
import { BinariesState, FetchStatus } from "./types";

const initialBinariesState: BinariesState = {
  fetchStatus: FetchStatus.idle,
  binaries: [],
};

export const binariesSlice = createSlice({
  name: "binaries",
  initialState: initialBinariesState,
  reducers: { ...actions },
});
