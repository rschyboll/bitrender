import { inject, injectable } from 'inversify';

import { UserView } from '@/schemas/user';
import { UserCreate } from '@/schemas/user';
import { Response, ServiceErrorType } from '@/services';
import { ApiEndpoints } from '@/services/endpoints';
import { IUserValidators } from '@/validators/interfaces';

import { IUserService } from '../interfaces';
import { Service } from './base';

@injectable()
export class UserService extends Service implements IUserService {
  private userValidators: IUserValidators;

  constructor(@inject(IUserValidators.$) userValidator: IUserValidators) {
    super();
    this.userValidators = userValidator;
  }

  public getCurrentUser = async (): Promise<Response<UserView>> => {
    try {
      const response = await this.api.get(ApiEndpoints.UserMe).json();
      if (this.userValidators.validateUserView(response)) {
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

  public login = async (
    username: string,
    password: string,
  ): Promise<Response<undefined>> => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    try {
      await this.api.post(ApiEndpoints.Login, {
        body: formData,
      });
      return { success: true, data: undefined };
    } catch (error: unknown) {
      return this.parseAPIError(error);
    }
  };

  public logged = async (): Promise<Response<boolean>> => {
    try {
      const response = await this.api.get(ApiEndpoints.Logged).json();
      if (typeof response == 'boolean') {
        return { success: true, data: response };
      } else {
        return {
          success: false,
          error: { type: ServiceErrorType.UnknownError },
        };
      }
    } catch (error: unknown) {
      return this.parseAPIError(error);
    }
  };

  public register = async (
    userCreate: UserCreate,
  ): Promise<Response<undefined>> => {
    try {
      await this.api.post(ApiEndpoints.Register, {
        json: userCreate,
      });
      return { success: true, data: undefined };
    } catch (error: unknown) {
      return this.parseAPIError(error);
    }
  };

  public logout = async (): Promise<Response<undefined>> => {
    try {
      await this.api.post(ApiEndpoints.Logout);
      return { success: true, data: undefined };
    } catch (error: unknown) {
      return this.parseAPIError(error);
    }
  };
}
