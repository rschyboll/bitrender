import config from '@/config';
import type { ListenersDef } from '@/logic/types';
import { ServiceErrorType } from '@/services';
import { sleep } from '@/utils/async';

import type { RoleUserCountLoaderLogic } from './type';

export const Listeners: ListenersDef<RoleUserCountLoaderLogic> = ({
  deps,
  actions,
  values,
}) => ({
  refresh: async () => {
    actions.load({ id: values.id });
  },

  loadSuccess: async ({ value }) => {
    if (values.entry != null) {
      deps.roleUserCountContainerLogic.actions.updateEntries({
        [values.id]: value,
      });
    } else {
      deps.roleUserCountContainerLogic.actions.addEntries({
        [values.id]: value,
      });
      deps.roleUserCountContainerLogic.actions.useEntries([values.id]);
    }
  },
  loadFailure: async ({ error }) => {
    if (
      error?.type == ServiceErrorType.ApiError ||
      (error?.type == ServiceErrorType.HTTPError && error.status == 404)
    ) {
      return;
    }
    await sleep(config.loadDelay);
    actions.load({ id: values.id });
  },
});
