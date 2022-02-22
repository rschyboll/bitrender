import { call, put, takeEvery, StrictEffect } from "redux-saga/effects";
import { PayloadAction } from "@reduxjs/toolkit";

import Axios from "axiosInstance";
import { binariesSlice } from "./reducer";
import { binariesValidator } from "./validators";

export function* binariesSaga() {
  yield takeEvery(binariesSlice.actions.fetchStart, getBinaries);
  yield takeEvery(binariesSlice.actions.addNewBinary, pushNewBinary);
  yield takeEvery(binariesSlice.actions.deleteBinary, deleteBinary);
}

function* getBinaries(): Generator<StrictEffect<any, any>, void, any> {
  try {
    const response = yield call(fetchBinaries);
    if (response.status !== 200) {
      throw Error();
    }
    const data = response.data;
    if (binariesValidator(data)) {
      yield put(binariesSlice.actions.fetchSuccess(data));
    }
  } catch (error) {
    yield put(binariesSlice.actions.fetchError());
  }
}

async function fetchBinaries() {
  const response = await Axios.get("/binaries/");
  return response;
}

function* pushNewBinary(
  action: PayloadAction<{ url: string; version: string }>
): Generator<StrictEffect<any, any>, void, any> {
  try {
    const response = yield call(
      pushBinary,
      action.payload.url,
      action.payload.version
    );
    if (response.status === 201) {
      yield put(binariesSlice.actions.fetchStart());
    }
  } catch (error) {}
}

async function pushBinary(url: string, version: string) {
  const response = await Axios.post("/binaries/new", {
    url: url,
    version: version,
  });
  return response;
}

function* deleteBinary(
  action: PayloadAction<{ id: string }>
): Generator<StrictEffect<any, any>, void, any> {
  try {
    const response = yield call(deleteBin, action.payload.id);
    if (response.status === 200) {
      yield put(binariesSlice.actions.fetchStart());
    }
  } catch (error) {}
}

async function deleteBin(id: string) {
  const response = await Axios.delete(`/binaries/delete?binary_id=${id}`);
  return response;
}
