import { FunctionComponent, useEffect } from "react";
import { useDispatch } from "react-redux";

import { workersSlice } from "store/workers/reducer";
import { workersSelectors } from "store/workers/selectors";
import { FetchStatus } from "store/workers/types";

import { WorkersView } from "./view";
import "./style.scss";

export type WorkersProps = {};

export const Workers: FunctionComponent<WorkersProps> = () => {
  const dispatch = useDispatch();
  const workers = workersSelectors.useWorkersData();
  const fetchStatus = workersSelectors.useWorkersFetchStatus();

  const activateWorker = (id: string) => {
    dispatch(workersSlice.actions.activate({ id: id }));
  };

  useEffect(() => {
    dispatch(workersSlice.actions.fetchStart());
  }, [dispatch]);

  return (
    <WorkersView
      workers={workers}
      loading={fetchStatus === FetchStatus.loading}
      activateWorker={activateWorker}
    />
  );
};
