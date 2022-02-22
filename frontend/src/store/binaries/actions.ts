import { PayloadAction } from "@reduxjs/toolkit";
import { BinariesState, FetchStatus, BinaryData } from "./types";

export const actions = {
  fetchStart: (state: BinariesState) => {
    state.fetchStatus = FetchStatus.loading;
  },
  fetchSuccess: (state: BinariesState, action: PayloadAction<BinaryData[]>) => {
    state.fetchStatus = FetchStatus.success;
    state.binaries = action.payload;
  },
  fetchError: (state: BinariesState) => {
    state.fetchStatus = FetchStatus.error;
  },
  addNewBinary: (
    state: BinariesState,
    action: PayloadAction<{ url: string; version: string }>
  ) => {},
  deleteBinary: (
    state: BinariesState,
    action: PayloadAction<{ id: string }>
  ) => {},
};
