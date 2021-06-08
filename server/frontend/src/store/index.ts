import { configureStore } from "@reduxjs/toolkit";

export const store = configureStore({
  reducer: {},
});

export type StoreState = ReturnType<typeof store.getState>;
