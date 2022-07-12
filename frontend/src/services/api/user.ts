import { inject } from 'inversify';
import { HTTPError } from 'ky';

import type { Response } from '@/services';
import { UserView, UserViewResponse } from '@/types/user';
import { IUserValidators } from '@/validators/interfaces';

import { Service } from '.';
import { IUserService } from '../interfaces';

export class UserService extends Service implements IUserService {
  private userValidator: IUserValidators;

  constructor(@inject(IUserValidators.$) userValidator: IUserValidators) {
    super();
    this.userValidator = userValidator;
  }

  public async getMe(): Promise<Response<UserView>> {
    try {
      const response = await this.api.get('/me').json();
    } catch (error) {
      console.log(error);
    }

    const testt = 1;

    return {
      success: false,
      error: {
        detail: '',
      },
    };
  }

  private userViewResponseToUserView(user: UserViewResponse): UserView {
    return {
      ...user,
      modifiedAt: new Date(user.modified_at),
      createdAt: new Date(user.created_at),
    };
  }
}
