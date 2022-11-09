import { decodeParams } from 'kea-router';

import type { SelectorsDef } from '@/logic/types';

import type { RouteLogicType } from './type';

export const Selectors: SelectorsDef<RouteLogicType> = {
  pathname: [
    (selectors) => [selectors.currentLocation],
    (currentLocation) => {
      return currentLocation.pathname;
    },
  ],
  search: [
    (selectors) => [selectors.currentLocation],
    (currentLocation) => {
      return currentLocation.search;
    },
  ],
  hash: [
    (selectors) => [selectors.currentLocation],
    (currentLocation) => {
      return currentLocation.hash;
    },
  ],
  state: [
    (selectors) => [selectors.currentLocation],
    (currentLocation) => {
      return currentLocation.state;
    },
  ],
  key: [
    (selectors) => [selectors.currentLocation],
    (currentLocation) => {
      return currentLocation.key;
    },
  ],
  searchParams: [
    (selectors) => [selectors.search],
    (search) => {
      return decodeParams(search, '?') as Record<string, unknown>;
    },
  ],
  hashParams: [
    (selectors) => [selectors.hash],
    (hash) => {
      return decodeParams(hash, '#') as Record<string, unknown>;
    },
  ],
};
