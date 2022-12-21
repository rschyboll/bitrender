import {
  actions,
  afterMount,
  kea,
  key,
  listeners,
  path,
  propsChanged,
  reducers,
  selectors,
} from 'kea';
import { subscriptions } from 'kea-subscriptions';
import { range } from 'lodash';

import { connect, deps, requests } from '@/logic/builders';
import { IRoleViewContainerLogic } from '@/logic/interfaces';
import { IRoleService } from '@/services/interfaces';

import { Listeners } from './listeners';
import { Reducers } from './reducers';
import { Selectors } from './selectors';
import { RoleVirtualLoaderLogic } from './type';

export const roleVirtualLoaderLogic = kea<RoleVirtualLoaderLogic>([
  path(['roles', 'loader', 'virtual']),
  key((props) => props.key),
  deps({
    roleService: IRoleService.$,
    roleViewContainerLogic: IRoleViewContainerLogic.$,
  }),
  connect(({ deps }) => [deps.roleViewContainerLogic]),
  actions({
    addLoadedEntryIds: (entryIds, offset) => ({ entryIds, offset }),
    setEntryRowCount: (rowCount) => ({
      rowCount,
    }),
    refresh: true,
  }),
  requests(({ deps }) => ({
    load: deps.roleService.getTable,
  })),
  reducers(Reducers),
  selectors(Selectors),
  listeners(Listeners),
  propsChanged(({ props, actions, values }) => {
    const neededIndexes = range(props.beginning, props.end);

    const notLoadedIndexes = neededIndexes.filter(
      (index) => !values.loadedEntryIds.has(index),
    );
    if (notLoadedIndexes.length != 0) {
      actions.refresh();
    }
  }),
  afterMount(({ actions }) => {
    actions.refresh();
  }),
]);
