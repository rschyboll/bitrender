import { useSelector } from "react-redux";

import { StoreState } from "store";
import { WorkerData, FetchStatus } from "./types";

export const workersSelectors = {
  useWorkersData: () => {
    return useSelector<StoreState, WorkerData[]>((state) => {
      return state.workers.workers;
    });
  },
  useWorkersFetchStatus: () => {
    return useSelector<StoreState, FetchStatus>((state) => {
      return state.workers.fetchStatus;
    });
  },
};
