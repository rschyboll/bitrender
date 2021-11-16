import { call, put, takeEvery, StrictEffect } from "redux-saga/effects";

import Axios from "axiosInstance";
import { tasksSlice } from "./reducer";
import { tasksValidator } from "./validators";

export function* tasksSaga() {
  yield takeEvery(tasksSlice.actions.fetchStart, getTasks);
}

function* getTasks(): Generator<StrictEffect<any, any>, void, any> {
  try {
    const response = yield call(fetchTasks);
    if (response.status !== 200) {
      throw Error();
    }
    const data = response.data;
    if (tasksValidator(data)) {
      yield put(tasksSlice.actions.fetchSuccess(data));
    }
  } catch (error) {
    yield put(tasksSlice.actions.fetchError());
  }
}

async function fetchTasks() {
  const response = await Axios.get("/tasks/");
  return response;
}
