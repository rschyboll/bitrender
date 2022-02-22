export enum FetchStatus {
  idle,
  loading,
  error,
  success,
}

export type TaskData = {
  id: string;
  name: string;
  samples: number;
  start_frame: number;
  end_frame: number;
  resolution_x: number;
  resolution_y: number;
  finished: boolean;
  packed: boolean;
};

export type TasksState = {
  fetchStatus: FetchStatus;
  tasks: TaskData[];
};
