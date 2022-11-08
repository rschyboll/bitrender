import { actions, kea, listeners, path, reducers, selectors } from "kea";

import type { RolesManagementLogic } from "./type";

export const rolesTableLogic = kea<RolesManagementLogic>([
  path(["roles", "management"]),
  actions({}),
  reducers({}),
  selectors(({ props }) => ({})),
  reducers({}),
  listeners(({ props, values, actions }) => ({})),
]);
