import {
  PaginatorCurrentPageReportOptions,
  PaginatorFirstPageLinkOptions,
  PaginatorJumpToPageInputOptions,
  PaginatorLastPageLinkOptions,
  PaginatorNextPageLinkOptions,
  PaginatorPageLinksOptions,
  PaginatorPrevPageLinkOptions,
  PaginatorRowsPerPageDropdownOptions,
  PaginatorTemplate as PrimePaginatorTemplate,
} from 'primereact/paginator';
import { memo } from 'react';

import './style.scss';

const FirstPageLink = memo(function FirstPageLink(
  props: PaginatorFirstPageLinkOptions,
) {
  return <div></div>;
});

const PrevPageLink = memo(function PrevPageLink(
  props: PaginatorPrevPageLinkOptions,
) {
  return <div></div>;
});

const PageLinks = memo(function PageLinks(props: PaginatorPageLinksOptions) {
  return <div></div>;
});

const NextPageLink = memo(function NextPageLink(
  props: PaginatorNextPageLinkOptions,
) {
  return <div></div>;
});

const LastPageLink = memo(function LastPageLink(
  props: PaginatorLastPageLinkOptions,
) {
  return <div></div>;
});

const RowsPerPageDropdown = memo(function RowsPerPageDropdown(
  props: PaginatorRowsPerPageDropdownOptions,
) {
  return <div></div>;
});

const CurrentPageReport = memo(function CurrentPageReport(
  props: PaginatorCurrentPageReportOptions,
) {
  return <div></div>;
});

const JumpToPageInput = memo(function JumpToPageInput(
  props: PaginatorJumpToPageInputOptions,
) {
  return <div></div>;
});

export const PaginatorTemplate: PrimePaginatorTemplate = {
  layout:
    'FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown CurrentPageReport',
  FirstPageLink: FirstPageLink,
  PrevPageLink: PrevPageLink,
  PageLinks: PageLinks,
  NextPageLink: NextPageLink,
  LastPageLink: LastPageLink,
  RowsPerPageDropdown: RowsPerPageDropdown,
  CurrentPageReport: CurrentPageReport,
  JumpToPageInput: JumpToPageInput,
};
