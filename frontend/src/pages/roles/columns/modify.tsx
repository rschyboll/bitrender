import { memo } from "react";

import { MRole } from "@/types/models";

export interface ModifyColumnProps {
  value: MRole.TableView;
}

export const ModifyColumn = memo(function ModifyColumn(
  props: ModifyColumnProps
) {
  return <div></div>;
});
