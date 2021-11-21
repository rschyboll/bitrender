import { call, put, takeEvery, StrictEffect } from "redux-saga/effects";
import { PayloadAction } from "@reduxjs/toolkit";

import Axios from "axiosInstance";
import { workersSlice } from "./reducer";
import { workersValidator } from "./validators";

export function* workersSaga() {
  yield takeEvery(workersSlice.actions.fetchStart, getWorkers);
  yield takeEvery(workersSlice.actions.activate, activateWorker);
}

function* getWorkers(): Generator<StrictEffect<any, any>, void, any> {
  try {
    const response = yield call(fetchWorkers);
    if (response.status !== 200) {
      throw Error();
    }
    const data = response.data;
    console.log(data);
    console.log(workersValidator(data));
    if (workersValidator(data)) {
      yield put(workersSlice.actions.fetchSuccess(data));
    }
  } catch (error) {
    yield put(workersSlice.actions.fetchError());
  }
}

async function fetchWorkers() {
  const response = await Axios.get("/workers/");
  return response;
}

function* activateWorker(
  action: PayloadAction<{ id: string }>
): Generator<StrictEffect<any, any>, void, any> {
  try {
    const response = yield call(pushActivation, { id: action.payload.id });
  } catch (error) {}
  yield call(getWorkers);
}

async function pushActivation(data: { id: string }) {
  const response = await Axios.post("workers/activate", {
    worker_id: data.id,
    status: true,
  });
  return response;
}
