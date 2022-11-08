import { enableMapSet } from "immer";
import { resetContext } from "kea";
import { localStoragePlugin } from "kea-localstorage";
import { subscriptionsPlugin } from "kea-subscriptions";

import Dependencies from "@/deps";
import { ISettingsLogic } from "@/logic/interfaces";

import { IRouteLogic } from "./interfaces/route";

export * from "./types";

export const startKea = () => {
  enableMapSet();
  resetContext({
    plugins: [subscriptionsPlugin, localStoragePlugin],
  });
};

export const startGlobalLogics = () => {
  Dependencies.get(ISettingsLogic.$).mount();
  Dependencies.get(IRouteLogic.$).mount();
};
