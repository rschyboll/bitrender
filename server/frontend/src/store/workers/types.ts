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
  subtask_id?: string;
  test_id?: string;
  composite_task_id?: string;
};

export type WorkersState = {
  fetchStatus: FetchStatus;
  workers: WorkerData[];
};
