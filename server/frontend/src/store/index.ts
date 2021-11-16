import { configureStore, combineReducers } from "@reduxjs/toolkit";
import createSagaMiddleware from "redux-saga";

import { binariesSlice } from "./binaries/reducer";
import { binariesSaga } from "./binaries/saga";
import { workersSlice } from "./workers/reducer";
import { workersSaga } from "./workers/saga";
import { tasksSlice } from "./tasks/reducer";
import { tasksSaga } from "./tasks/saga";

const sagaMiddleWare = createSagaMiddleware();

const reducer = combineReducers({
  binaries: binariesSlice.reducer,
  workers: workersSlice.reducer,
  tasks: tasksSlice.reducer,
});

export const store = configureStore({
  reducer: reducer,
  middleware: [sagaMiddleWare],
});

sagaMiddleWare.run(binariesSaga);
sagaMiddleWare.run(workersSaga);
sagaMiddleWare.run(tasksSaga);

export type StoreState = ReturnType<typeof store.getState>;
