import { useSelector } from "react-redux";

import { StoreState } from "store";
import { BinaryData, FetchStatus } from "./types";

export const binariesSelectors = {
  useBinariesData: () => {
    return useSelector<StoreState, BinaryData[]>((state) => {
      return state.binaries.binaries;
    });
  },
  useBinariesFetchStatus: () => {
    return useSelector<StoreState, FetchStatus>((state) => {
      return state.binaries.fetchStatus;
    });
  },
};
