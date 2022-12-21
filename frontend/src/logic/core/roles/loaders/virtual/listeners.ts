import config from '@/config';
import type { ListenersDef } from '@/logic/types';
import { ServiceErrorType } from '@/services';
import { sleep } from '@/utils/async';

import type { RoleVirtualLoaderLogic } from './type';

export const Listeners: ListenersDef<RoleVirtualLoaderLogic> = ({
  actions,
  props,
  deps,
}) => ({
  refresh: async (_, breakpoint) => {
    await breakpoint(250);
    if (props.end == 0) {
      return;
    }
    actions.load({
      page_or_range: {
        beginning: props.beginning,
        end: props.end,
      },
      search: [],
    });
  },
  loadSuccess: async ({ value }) => {
    const entryIds = value.items.map((roleView) => {
      return roleView.id;
    });

    actions.setEntryRowCount(value.rowCount);
    actions.addLoadedEntryIds(entryIds, props.beginning);
    deps.roleViewContainerLogic.actions.addEntries(value.items);
    deps.roleViewContainerLogic.actions.useEntries(entryIds);
  },
  loadFailure: async ({ error }) => {
    if (error?.type == ServiceErrorType.ApiError) {
      return;
    }
    await sleep(config.loadDelay);
    actions.refresh();
  },
});
