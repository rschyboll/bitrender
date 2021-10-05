import { configureStore, combineReducers } from "@reduxjs/toolkit";
import createSagaMiddleware from "redux-saga";

import { binariesSlice } from "./binaries/reducer";
import { binariesSaga } from "./binaries/saga";

const sagaMiddleWare = createSagaMiddleware();

const reducer = combineReducers({
  binaries: binariesSlice.reducer,
});

export const store = configureStore({
  reducer: reducer,
  middleware: [sagaMiddleWare],
});

sagaMiddleWare.run(binariesSaga);

export type StoreState = ReturnType<typeof store.getState>;
