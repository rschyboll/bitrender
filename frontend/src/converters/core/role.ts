import { injectable } from 'inversify';
import type { PartialRecord } from 'kea';

import type { IRoleConverters } from '@/converters/interfaces';
import { MRole } from '@/types/models';

@injectable()
export class RoleConverters implements IRoleConverters {
  public viewToTableView(view: MRole.View): MRole.TableView {
    const permissions: PartialRecord<MRole.Permission, boolean> = {};

    Object.values(MRole.Permission).map((permission) => {
      if (permission in view.permissions) {
        permissions[permission] = true;
      } else {
        permissions[permission] = false;
      }
    });

    return {
      id: view.id,
      name: view.name,
      default: view.default,
      ...(permissions as Record<MRole.Permission, boolean>),
    };
  }
}
