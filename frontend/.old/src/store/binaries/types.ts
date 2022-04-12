export enum FetchStatus {
  idle,
  loading,
  error,
  success,
}

export type BinaryData = {
  id: string;
  version: string;
  url: string;
};

export type BinariesState = {
  fetchStatus: FetchStatus;
  binaries: BinaryData[];
};
