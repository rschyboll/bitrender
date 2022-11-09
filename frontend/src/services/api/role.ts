import { inject, injectable } from 'inversify';

import { Response, ServiceErrorType } from '@/services';
import { ApiEndpoints } from '@/services/endpoints';
import { MRole } from '@/types/models';
import { IRoleValidators } from '@/validators/interfaces';

import { IRoleService } from '../interfaces';
import { Service } from './base';

@injectable()
export class RoleService extends Service implements IRoleService {
  private roleValidators: IRoleValidators;

  constructor(@inject(IRoleValidators.$) roleValidators: IRoleValidators) {
    super();
    this.roleValidators = roleValidators;
  }

  public getRoles = async (
    input: MRole.Messages.GetRolesInput,
  ): Promise<Response<MRole.Messages.GetRolesOutput>> => {
    try {
      const response = await this.api
        .get(ApiEndpoints.Roles + '?' + this.listRequestToURL(input))
        .json();
      if (this.roleValidators.validateGetRolesOutput(response)) {
        return { success: true, data: response };
      }
      return {
        success: false,
        error: {
          type: ServiceErrorType.ValidationError,
        },
      };
    } catch (error: unknown) {
      return this.parseAPIError(error);
    }
  };
}
