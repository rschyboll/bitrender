export enum FetchStatus {
  idle,
  loading,
  error,
  success,
}

export type WorkerData = {
  id: string;
  name: string;
  register_date: string;
  active: boolean;
  test_time?: number;
};

export type WorkersState = {
  fetchStatus: FetchStatus;
  workers: WorkerData[];
};
