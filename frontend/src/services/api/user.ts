import { inject, injectable } from 'inversify';

import type { Response } from '@/types/service';
import { ServiceErrorType } from '@/types/service';
import { UserView, UserViewResponse } from '@/types/user';
import { IUserValidators } from '@/validators/interfaces';

import { IUserService } from '../interfaces';
import { Service } from './base';

@injectable()
export class UserService extends Service implements IUserService {
  private userValidator: IUserValidators;

  constructor(@inject(IUserValidators.$) userValidator: IUserValidators) {
    super();
    this.userValidator = userValidator;
  }

  public async getCurrentUser(): Promise<Response<UserView>> {
    try {
      const response = await this.api.get('user/me').json();
      if (this.userValidator.validateUserViewResponse(response)) {
        return {
          success: true,
          data: this.userViewResponseToUserView(response),
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

  private userViewResponseToUserView(user: UserViewResponse): UserView {
    return {
      ...user,
      modifiedAt: new Date(user.modified_at),
      createdAt: new Date(user.created_at),
    };
  }
}
