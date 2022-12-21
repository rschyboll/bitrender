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

  public getTable = async (
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

  public getById = async (
    input: MRole.Messages.GetByIdInput,
  ): Promise<Response<MRole.Messages.GetByIdOutput>> => {
    try {
      const response = await this.api
        .get(ApiEndpoints.RoleGetById(input.id))
        .json();
      if (this.roleValidators.validateGetByIdOutput(response)) {
        return { success: true, data: response };
      } else {
        return {
          success: false,
          error: {
            type: ServiceErrorType.ValidationError,
          },
        };
      }
    } catch (error: unknown) {
      return this.parseAPIError(error);
    }
  };

  public getUserCount = async (
    input: MRole.Messages.GetUserCountInput,
  ): Promise<Response<MRole.Messages.GetUserCountOutput>> => {
    try {
      const response = await this.api
        .get(ApiEndpoints.RoleGetUserCount(input.id))
        .json();
      if (this.roleValidators.validateGetUserCountOutput(response)) {
        return { success: true, data: response };
      } else {
        return {
          success: false,
          error: {
            type: ServiceErrorType.ValidationError,
          },
        };
      }
    } catch (error: unknown) {
      return this.parseAPIError(error);
    }
  };

  public delete = async (
    input: MRole.Messages.DeleteInput,
  ): Promise<Response<void>> => {
    try {
      await this.api.delete(ApiEndpoints.RoleDelete(input.id));
      return { success: true, data: undefined };
    } catch (error: unknown) {
      return this.parseAPIError(error);
    }
  };
}
