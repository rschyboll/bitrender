import { injectable } from 'inversify';
import { PartialRecord } from 'kea';

import { IRoleConverters } from '@/converters/interfaces';
import { Permission, RoleTableView, RoleView } from '@/schemas/role';

@injectable()
export class RoleConverters implements IRoleConverters {
  public viewToTableView(view: RoleView): RoleTableView {
    const permissions: PartialRecord<Permission, true | null> = {};

    Object.values(Permission).map((permission) => {
      if (permission in view.permissions) {
        permissions[permission] = true;
      } else {
        permissions[permission] = null;
      }
    });

    return {
      name: view.name,
      default: view.default,
      ...(permissions as Record<Permission, true | null>),
    };
  }
}
