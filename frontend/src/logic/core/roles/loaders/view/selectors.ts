import type { SelectorsDef } from '@/logic/types';

import type { RoleViewLoaderLogic } from './type';

export const Selectors: SelectorsDef<RoleViewLoaderLogic> = ({ deps }) => ({
  id: [(_, props) => [props.id], (id) => id],
  entry: [
    (selectors) => [
      deps.roleViewContainerLogic.selectors.entries,
      selectors.id,
    ],
    (entries, uuid) => {
      const entry = entries.get(uuid);
      if (entry != null) {
        return entry;
      } else {
        return null;
      }
    },
  ],
});
