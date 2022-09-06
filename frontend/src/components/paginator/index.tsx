import { Button } from 'primereact/button';
import {
  PaginatorCurrentPageReportOptions,
  PaginatorFirstPageLinkOptions,
  PaginatorLastPageLinkOptions,
  PaginatorNextPageLinkOptions,
  PaginatorPrevPageLinkOptions,
  PaginatorRowsPerPageDropdownOptions,
  PaginatorTemplate as PrimePaginatorTemplate,
} from 'primereact/paginator';
import { classNames } from 'primereact/utils';
import { memo } from 'react';
import { Trans, useTranslation } from 'react-i18next';
import {
  FiChevronLeft,
  FiChevronRight,
  FiChevronsLeft,
  FiChevronsRight,
} from 'react-icons/fi';

import { Dropdown } from '../dropdown';
import './style.scss';

const FirstPageLink = memo(function FirstPageLink(
  props: PaginatorFirstPageLinkOptions,
) {
  return (
    <Button
      type="button"
      className={classNames('p-paginator-first p-paginator-element p-link', {
        'p-disabled': props.disabled,
      })}
      icon={
        <FiChevronsLeft
          className="p-paginator-icon"
          size="1.5rem"
          style={{ transform: 'translateX(-1px)' }}
        />
      }
      onClick={props.onClick}
      disabled={props.disabled}
    />
  );
});

const PrevPageLink = memo(function PrevPageLink(
  props: PaginatorPrevPageLinkOptions,
) {
  return (
    <Button
      type="button"
      className={classNames('p-paginator-first p-paginator-element p-link', {
        'p-disabled': props.disabled,
      })}
      icon={
        <FiChevronLeft
          className="p-paginator-icon"
          size="1.5rem"
          style={{ transform: 'translateX(-1px)' }}
        />
      }
      onClick={props.onClick}
      disabled={props.disabled}
    />
  );
});

const NextPageLink = memo(function NextPageLink(
  props: PaginatorNextPageLinkOptions,
) {
  return (
    <Button
      type="button"
      className={classNames('p-paginator-first p-paginator-element p-link', {
        'p-disabled': props.disabled,
      })}
      icon={
        <FiChevronRight
          className="p-paginator-icon"
          size="1.5rem"
          style={{ transform: 'translateX(-1px)' }}
        />
      }
      onClick={props.onClick}
      disabled={props.disabled}
    />
  );
});

const LastPageLink = memo(function LastPageLink(
  props: PaginatorLastPageLinkOptions,
) {
  return (
    <Button
      type="button"
      className={classNames('p-paginator-first p-paginator-element p-link', {
        'p-disabled': props.disabled,
      })}
      icon={
        <FiChevronsRight
          className="p-paginator-icon"
          size="1.5rem"
          style={{ transform: 'translateX(0.5px)' }}
        />
      }
      onClick={props.onClick}
      disabled={props.disabled}
    />
  );
});

const RowsPerPageDropdown = memo(function RowsPerPageDropdown(
  props: PaginatorRowsPerPageDropdownOptions,
) {
  const dropdownOptions = [
    { label: 10, value: 10 },
    { label: 20, value: 20 },
    { label: 30, value: 30 },
  ];

  return (
    <div className="paginator-rows-per-page">
      <span>
        <Trans>itemsPerPage</Trans>
      </span>
      <Dropdown
        value={props.value}
        options={dropdownOptions}
        onChange={props.onChange}
      />
    </div>
  );
});

const CurrentPageReport = memo(function CurrentPageReport(
  props: PaginatorCurrentPageReportOptions,
) {
  const { t } = useTranslation();

  return (
    <span className="paginator-current-page-report">
      {t('currentPageReport', {
        replace: {
          first: props.first,
          last: props.last,
          all: props.totalRecords,
        },
      })}
    </span>
  );
});

export const PaginatorTemplate: PrimePaginatorTemplate = {
  layout:
    'CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown',
  FirstPageLink: (options) => <FirstPageLink {...options} />,
  PrevPageLink: (options) => <PrevPageLink {...options} />,
  NextPageLink: (options) => <NextPageLink {...options} />,
  LastPageLink: (options) => <LastPageLink {...options} />,
  RowsPerPageDropdown: (options) => <RowsPerPageDropdown {...options} />,
  CurrentPageReport: (options) => <CurrentPageReport {...options} />,
} as PrimePaginatorTemplate;
