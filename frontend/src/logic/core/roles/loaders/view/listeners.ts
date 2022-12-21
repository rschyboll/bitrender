import config from '@/config';
import type { ListenersDef } from '@/logic/types';
import { ServiceErrorType } from '@/services';
import { sleep } from '@/utils/async';

import type { RoleViewLoaderLogic } from './type';

export const Listeners: ListenersDef<RoleViewLoaderLogic> = ({
  deps,
  actions,
  values,
}) => ({
  refresh: async () => {
    actions.load({ id: values.id });
  },
  loadSuccess: async ({ value }) => {
    if (values.entry != null) {
      deps.roleViewContainerLogic.actions.updateEntries([value]);
    } else {
      deps.roleViewContainerLogic.actions.addEntries([value]);
      deps.roleViewContainerLogic.actions.useEntries([value.id]);
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
