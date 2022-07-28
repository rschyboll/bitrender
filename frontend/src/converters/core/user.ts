import { injectable } from 'inversify';

import { UserView, UserViewResponse } from '@/types/user';

@injectable()
export class UserConverters {
  public userViewResponseToUserView(viewResponse: UserViewResponse): UserView {
    return {
      ...viewResponse,
      modifiedAt: new Date(viewResponse.modified_at),
      createdAt: new Date(viewResponse.created_at),
    };
  }
}
