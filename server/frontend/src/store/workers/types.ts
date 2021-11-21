export enum FetchStatus {
  idle,
  loading,
  error,
  success,
}

export type WorkerData = {
  id: string;
  create_date: string;
  name: string;
  active: boolean;
  subtask_id?: number;
  test_id?: number;
};

export type WorkersState = {
  fetchStatus: FetchStatus;
  workers: WorkerData[];
};
