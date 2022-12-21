export enum SortOrder {
  ASC = 0,
  DESC = 1,
}

export enum SearchRule {
  EQUAL = 0,
  NOTEQUAL = 1,
  BEGINSWITH = 2,
  GREATER = 3,
  GREATEROREQUAL = 4,
  LESS = 5,
  LESSOREQUAL = 6,
  CONTAINS = 7,
}

export interface ListRequestSort<Columns extends string> {
  column: Columns;
  order: SortOrder;
}

export interface ListRequestSearch<Columns extends string> {
  column: Columns;
  rule: SearchRule;
  value: number | string | null;
}

export interface ListRequestPage {
  recordsPerPage: number;
  pageNr: number;
}

export interface ListRequestRange {
  beginning: number;
  end: number;
}

export interface ListRequestInput<Columns extends string> {
  sort?: ListRequestSort<Columns>;
  search: ListRequestSearch<Columns>[];
  page_or_range?: ListRequestPage | ListRequestRange;
}

export interface ListRequestOutput<Items> {
  items: Items;
  rowCount: number;
}
