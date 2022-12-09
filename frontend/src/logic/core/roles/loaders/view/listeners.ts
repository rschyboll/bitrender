import config from '@/config';
import type { ListenersDef } from '@/logic/types';
import { sleep } from '@/utils/async';

import type { RoleViewLoaderLogic } from './type';

export const Listeners: ListenersDef<RoleViewLoaderLogic> = ({
  deps,
  actions,
  values,
}) => ({
  loadSuccess: async ({ value }) => {
    deps.roleViewContainerLogic.actions.addEntries([value]);
    deps.roleViewContainerLogic.actions.useEntries([value.id]);
  },
  loadFailure: async () => {
    await sleep(config.loadDelay);
    actions.load({ id: values.id });
  },
});
