import { inject, injectable } from 'inversify';

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
      return this.parseAPIError(error);
    }
  }
}
