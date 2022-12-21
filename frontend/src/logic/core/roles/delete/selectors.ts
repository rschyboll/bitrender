import type { SelectorsDef } from '@/logic/types';

import type { RoleDeleteLogic } from './type';

export const Selectors: SelectorsDef<RoleDeleteLogic> = ({ deps }) => ({
  id: [(_, props) => [props.id], (id) => id],
  view: [() => [deps.roleViewLoaderLogic.selectors.entry], (view) => view],
  viewLoadStatus: [
    () => [deps.roleViewLoaderLogic.selectors.loadStatus],
    (status) => status,
  ],
  viewLoadError: [
    () => [deps.roleViewLoaderLogic.selectors.loadError],
    (error) => error,
  ],
  userCount: [
    () => [deps.roleUserCountLoaderLogic.selectors.entry],
    (userCount) => userCount,
  ],
  userCountLoadStatus: [
    () => [deps.roleUserCountLoaderLogic.selectors.loadStatus],
    (status) => status,
  ],
  userCountLoadError: [
    () => [deps.roleUserCountLoaderLogic.selectors.loadError],
    (error) => error,
  ],
});
