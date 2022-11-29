import type { SelectorsDef } from '@/logic/types';
import { ListRequestInput, SearchRule } from '@/services/messages/list';
import { MRole } from '@/types/models';

import type { RolesTableLogic } from './type';

export const Selectors: SelectorsDef<RolesTableLogic> = ({ deps }) => ({
  values: [
    () => [deps.roleTableLoaderLogic.selectors.entries],
    (roles) => roles,
  ],
  searchString: [
    (selectors) => [
      selectors.localSearchString,
      deps.routeLogic.selectors.hashParams,
    ],
    (localSearchString, hashParams) => {
      const search = hashParams['search'];
      if (localSearchString == null) {
        if (typeof search == 'string') {
          return search;
        }
        return '';
      }
      return localSearchString;
    },
  ],
  rowsPerPage: [
    () => [deps.routeLogic.selectors.hashParams],
    (hashParams) => {
      const rows = hashParams['rows'];
      if (typeof rows == 'number') {
        return rows;
      }
      return 10;
    },
  ],
  currentPage: [
    () => [deps.routeLogic.selectors.hashParams],
    (hashParams) => {
      const page = hashParams['page'];
      if (typeof page == 'number') {
        return page;
      }
      return 0;
    },
  ],
  listRequestInput: [
    (selectors) => [
      selectors.currentPage,
      selectors.rowsPerPage,
      selectors.searchString,
    ],
    (currentPage, rowsPerPage, searchString) => {
      const listRequestInput: ListRequestInput<MRole.Columns> = {
        search: [
          {
            column: 'name',
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
