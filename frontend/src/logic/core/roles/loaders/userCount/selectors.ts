import type { SelectorsDef } from '@/logic/types';

import type { RoleUserCountLoaderLogic } from './type';

export const Selectors: SelectorsDef<RoleUserCountLoaderLogic> = ({
  deps,
}) => ({
  id: [(_, props) => [props.id], (id) => id],
  entry: [
    (selectors) => [
      deps.roleUserCountContainerLogic.selectors.entries,
      selectors.id,
    ],
    (entries, id) => {
      const entry = entries.get(id);
      if (entry != null) {
        return entry;
      }
      return null;
    },
  ],
});
