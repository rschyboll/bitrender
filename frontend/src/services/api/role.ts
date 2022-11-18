import { inject, injectable } from 'inversify';

import { Response, ServiceErrorType } from '@/services';
import { ApiEndpoints } from '@/services/endpoints';
import { MRole } from '@/types/models';
import { sleep } from '@/utils/async';
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

  public getList = async (
    input: MRole.Messages.GetListInput,
  ): Promise<Response<MRole.Messages.GetListOutput>> => {
    try {
      const response = await this.api
        .get(ApiEndpoints.Roles + '?' + this.listRequestToURL(input))
        .json();
      if (this.roleValidators.validateGetListOutput(response)) {
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

  public create = async (
    input: MRole.Messages.CreateInput,
  ): Promise<Response<MRole.Messages.CreateOutput>> => {
    await sleep(50000);
    try {
      const response = await this.api
        .post(ApiEndpoints.RoleNew, { json: input })
        .json();
      if (this.roleValidators.validateCreateOutput(response)) {
        return {
          success: true,
          data: response,
        };
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
