import { inject, injectable } from 'inversify';

import { ApiEndpoints } from '@/services/endpoints';
import type { GetRolesInput, GetRolesOutput } from '@/services/messages/role';
import type { Response } from '@/types/service';
import { ServiceErrorType } from '@/types/service';
import { IRoleValidators } from '@/validators/interfaces';

import { IRoleService } from '../interfaces';
import { Service } from './base';

@injectable()
export class RolesService extends Service implements IRoleService {
  private roleValidators: IRoleValidators;

  constructor(@inject(IRoleValidators.$) roleValidators: IRoleValidators) {
    super();
    this.roleValidators = roleValidators;
  }

  public async getRoles(
    input: GetRolesInput,
  ): Promise<Response<GetRolesOutput>> {
    try {
      const response = await this.api
        .get(ApiEndpoints.Roles + this.listRequestToURL(input))
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
  }
}
