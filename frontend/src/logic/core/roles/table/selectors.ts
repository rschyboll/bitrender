import type { SelectorsDef } from "@/logic/types";
import { MRole } from "@/types/models";

import type { RolesTableLogic } from "./type";

export const Selectors: SelectorsDef<RolesTableLogic> = ({ deps }) => ({
  values: [
    (selectors) => [selectors.roles],
    (roles) => {
      const roleTableViews = [];
      for (const role of roles) {
        roleTableViews.push(props.deps.roleConverters.viewToTableView(role));
      }
      return roleTableViews;
    },
  ],
  searchString: [
    (selectors) => [selectors.urlSearchString, selectors.localSearchString],
    (urlSearchString, localSearchString) => {
      if (localSearchString == null) {
        return urlSearchString;
      }
      return localSearchString;
    },
  ],
  urlSearchString: [
    () => [props.deps.routeLogic.selectors.hashParams],
    (hashParams) => {
      const search = hashParams["search"];
      if (typeof search == "string") {
        return search;
      }
      return "";
    },
  ],
  rowsPerPage: [
    () => [props.deps.routeLogic.selectors.hashParams],
    (hashParams) => {
      const rows = hashParams["rows"];
      if (typeof rows == "number") {
        return rows;
      }
      return 10;
    },
  ],
  currentPage: [
    () => [props.deps.routeLogic.selectors.hashParams],
    (hashParams) => {
      const page = hashParams["page"];
      if (typeof page == "number") {
        return page;
      }
      return 0;
    },
  ],
  listRequestInput: [
    (selectors) => [
      selectors.currentPage,
      selectors.rowsPerPage,
      selectors.urlSearchString,
    ],
    (currentPage, rowsPerPage, searchString) => {
      const listRequestInput: ListRequestInput<RoleColumns> = {
        search: [
          {
            column: "name",
            rule: SearchRule.CONTAINS,
            value: searchString,
          },
        ],
        page: {
          pageNr: currentPage,
          recordsPerPage: rowsPerPage,
        },
      };
      return listRequestInput;
    },
  ],
});
