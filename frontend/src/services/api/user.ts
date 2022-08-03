import { inject, injectable } from 'inversify';
import { HTTPError } from 'ky';

import { ApiEndpoints } from '@/services/endpoints';
import type { Response } from '@/types/service';
import { ServiceErrorType } from '@/types/service';
import { UserView } from '@/types/user';
import { IUserValidators } from '@/validators/interfaces';

import { IUserService } from '../interfaces';
import { IUserConverters } from './../../converters/interfaces/user';
import { Service } from './base';

@injectable()
export class UserService extends Service implements IUserService {
  private userValidators: IUserValidators;
  private userConverters: IUserConverters;

  constructor(
    @inject(IUserValidators.$) userValidator: IUserValidators,
    @inject(IUserConverters.$) userConverters: IUserConverters,
  ) {
    super();
    this.userValidators = userValidator;
    this.userConverters = userConverters;
  }

  public async getCurrentUser(): Promise<Response<UserView>> {
    try {
      const response = await this.api.get(ApiEndpoints.UserMe).json();
      if (this.userValidators.validateUserViewResponse(response)) {
        return {
          success: true,
          data: this.userConverters.userViewResponseToUserView(response),
        };
      }
      return {
        success: false,
        error: {
          type: ServiceErrorType.ValidationError,
        },
      };
    } catch (error: unknown) {
      console.log(error);
      return this.parseAPIError(error);
    }
  }

  public async login(
    username: string,
    password: string,
  ): Promise<Response<undefined>> {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    try {
      await this.api.post(ApiEndpoints.Login, {
        body: formData,
      });
      return { success: true, data: undefined };
    } catch (error: unknown) {
      if (error instanceof HTTPError) {
        console.log(await error.response.json());
      }
      return this.parseAPIError(error);
    }
  }
}
